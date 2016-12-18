# !/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function, division

import time
import six


class TableSuffix(object):
    def __init__(self, table_name, db, debug=False, union_number=0,
                 table_capacity=5000000):
        self.table_name = table_name
        self.debug = debug
        self.db = db

        self.init_status = 0

        self._create_table_sql = None
        self._union_number = union_number
        self._table_capacity = table_capacity
        self._child = 'ENGINE=MyISAM DEFAULT CHARSET=utf8'
        self._merge = ('ENGINE=MRG_MYISAM UNION=(%s) '
                       'INSERT_METHOD=LAST DEFAULT CHARSET=utf8')

    @property
    def table_suffix(self):
        """获取指定表的分表数量.
        """

        get_count_sql = (
            'SELECT table_count FROM table_division '
            'WHERE table_name = :table_name')

        params = dict(table_name=self.table_name)
        rs = self.db.execute(get_count_sql, params=params).fetchone()
        self.db.commit()

        return rs[0] if rs else 0

    @property
    def table_latest(self):
        """获取指定表的最新记录最大Id.
        """

        get_count_sql = (
            'SELECT max(id) '
            'FROM {table_name}').format(table_name=self.table_name)

        rs = self.db.execute(get_count_sql).fetchone()
        self.db.commit()

        return rs[0] if rs else 0

    def _get_table_capacity(self):
        return self._table_capacity

    def _set_table_capacity(self, value):
        if not isinstance(value, int):
            raise ValueError
        self._table_capacity = value

    table_capacity = property(_get_table_capacity,
                              _set_table_capacity,
                              doc='''Single Table Capacity.''')

    del _get_table_capacity, _set_table_capacity

    def _get_union_number(self):
        return self._union_number

    def _set_union_number(self, value):
        if not isinstance(value, int):
            raise ValueError
        self._union_number = value

    union_number = property(_get_union_number,
                            _set_union_number,
                            doc='''Merge Table Union Number.''')

    del _get_union_number, _set_union_number

    def _get_create_table_sql(self):
        return self._create_table_sql

    def _set_create_table_sql(self, value):
        if not isinstance(value, six.string_types):
            raise ValueError
        self._create_table_sql = value

    create_table_sql = property(_get_create_table_sql,
                                _set_create_table_sql,
                                doc='''Create Table SQL.''')

    del _get_create_table_sql, _set_create_table_sql

    def _update(self, child_num=1):
        """
            2 >> 分表后: 更新指定表的分表数量.
            3 >> 合表更新: 更新指定表的UNION.
        """

        # 2 >> 更新指定表的分表数量.
        print('2 >> Starting Update Record For %s.' % self.table_name)
        update_or_insert_sql = (
            'INSERT INTO table_division (table_name,  table_count) '
            'VALUES (:table_name,:child_num) '
            'ON DUPLICATE KEY UPDATE table_count = table_count + :child_num')

        params = dict(table_name=self.table_name, child_num=child_num)
        self.db.execute(update_or_insert_sql, params=params)

        # 3 >> 更新指定表的UNION.
        print('3 >> Starting Merge Child Tables For %s.' % self.table_name)
        name_suffix = self.table_suffix + child_num
        unions = ['%s_%s' % (self.table_name, i) for i in
                  range(1, name_suffix + 1)]

        # 挂载多少子表在总表下.
        if self.union_number:
            unions = unions[-self.union_number:]

        create_merge_sql = ''.join(
            (self.create_table_sql.format(table_suffix=''),
             self._merge % ','.join(unions)))

        self.db.execute(create_merge_sql)

    def work(self):
        """1 >> 分表建立: 创建指定表的子表.
        """

        if not self.create_table_sql:
            raise Exception("<Parameters:create_table_sql> Are Not Set!")

        print('1 >> Starting Create Child Tables For %s.' % self.table_name)
        name_suffix = self.table_suffix

        def create_child(index=1):
            print('  >> Create Child Table For %s_%s.' % (
                self.table_name, str(name_suffix + index)))

            create_child_sql = ''.join((
                self.create_table_sql, self._child)).format(
                table_suffix=''.join(('_', str(name_suffix + index))))

            self.db.execute(create_child_sql)

        # 判断使用场景, 如果无记录为最初原表.
        if not self.table_suffix:
            self.init_status = 1

            # 计算原表最新最大数据Id, 确定分多少子表.
            latest_max_id = self.table_latest
            table_total = latest_max_id / self.table_capacity
            if isinstance(table_total, float):
                table_total = int(table_total) + 1

            # 创建子表.
            for i in range(1, table_total + 1):
                create_child(i)

            return table_total
        else:
            self.init_status = 2
            create_child()
            return 1

    def run(self):
        try:
            child_num = self.work()
            if self.init_status == 1:
                # 备份: 备份指定表的原表.
                print('Backup Data: >> Rename Table For %s.' % self.table_name)

                backup_table_sql = (
                    'ALTER TABLE {old_name} RENAME TO  {new_name}').format(
                    old_name=self.table_name,
                    new_name='%s_bck' % self.table_name)
                self.db.execute(backup_table_sql)
            elif self.init_status == 2:
                # 备份: 备份原来的Merge表.
                back_merge_table = '%s_%s' % (self.table_name, time.time())
                print('Backup Merge: >> Rename %s To %s.' %
                      (self.table_name, back_merge_table))

                backup_table_sql = (
                    'ALTER TABLE {old_name} RENAME TO  {new_name}').format(
                    old_name=self.table_name,
                    new_name=back_merge_table)
                self.db.execute(backup_table_sql)

            self._update(child_num)
            self.db.commit()
        except Exception as ex:
            print(ex)
            self.db.rollback()
        else:
            if self.init_status == 1:
                # 初始化: 原表数据导入分表.
                print('Init Data: >> From Backup Import Data To Child Table.')

                for suffix_num in range(1, self.table_suffix + 1):
                    # TODO:分表的导入, 即使单表500万一次导入也可能造成MySQL高负载.
                    init_table_sql = (
                        "INSERT INTO {new_name} SELECT * FROM {old_name} "
                        "WHERE id > :start_id AND id <= :end_id"
                    ).format(
                        new_name='%s_%s' % (self.table_name, str(suffix_num)),
                        old_name='%s_bck' % self.table_name)

                    params = dict(
                        start_id=self.table_capacity * (suffix_num - 1),
                        end_id=self.table_capacity * suffix_num)

                    self.db.execute(init_table_sql, params=params)
                self.db.commit()

    def drop_table(self):
        """删除测试创建的表.
        """

        if self.debug:
            # 仅在Debug模式下允许删除操作,为方便开发者测试而用.
            drop_table_sql = 'DROP TABLE {table_name}_{suffix}'

            for suffix_num in range(self.table_suffix, 0, -1):
                self.db.execute(drop_table_sql.format(
                    table_name=self.table_name,
                    suffix=str(suffix_num)))
            self.db.commit()
