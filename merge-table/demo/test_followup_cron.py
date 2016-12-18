# !/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

from unittest import TestCase
from conf import debug, db_session
from table import FollowUP


class BaseTestCase(TestCase):
    # 填充测试数据.
    insert_sql = (
        "INSERT INTO `followup`(`category`,`codex`,`content`,`staff_id`,"
        "`student_id`,`type`,`next_contact_time`) "
        "VALUES(1,123,'hello,word',1,1,1,45534254)")

    def setUp(self):
        for _ in range(0, 100):
            db_session.execute(self.insert_sql)
        db_session.commit()

    def tearDown(self):
        db_session.execute('drop table followup')
        db_session.execute('alter table followup_bck rename to followup')
        db_session.execute('truncate table followup')
        db_session.execute('truncate table table_division')
        db_session.commit()

    def test_followup(self):
        # 1 >>> 首次分表
        followup = FollowUP('followup', db_session, debug=debug)

        # 分表的配置数据置前设置.
        followup.table_capacity = 30
        followup.union_number = 0

        # 1 >>>>>> 首次分表.
        followup.run()
        print('1 >>>>>> 首次分表 %s' % followup.table_suffix)
        assert followup.table_suffix == 4

        # 以下数据写入最后follow_4表.
        for _ in range(0, 10):
            db_session.execute(self.insert_sql)
        db_session.commit()

        # 2 >>>>>> CRON分表, 检测到新写入数据增新表follow_5.
        followup.run()
        print('2 >>>>>> CRON分表 %s' % followup.table_suffix)
        assert followup.table_suffix == 5

        # 以下数据写入最后follow_5表.
        for _ in range(0, 10):
            db_session.execute(self.insert_sql)
        db_session.commit()

        assert followup.table_latest == 120
        followup.drop_table()
