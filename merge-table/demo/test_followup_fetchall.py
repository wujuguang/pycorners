# !/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import sys
import time
from unittest import TestCase
from conf import db_session


class BaseTestCase(TestCase):
    # 填充测试数据.
    insert_sql = (
        "INSERT INTO `followup`(`category`,`codex`,`content`,`staff_id`,"
        "`student_id`,`type`,`next_contact_time`) "
        "VALUES(1,123,'hello,word',1,1,1,45534254)")

    select_sql = ('select id,staff_id, student_id, category, codex, '
                  'next_contact_time from `followup`')

    def setUp(self):
        for _ in range(0, 10000):
            db_session.execute(self.insert_sql)
        db_session.commit()

    def tearDown(self):
        db_session.execute('truncate table followup')
        db_session.commit()

    def test_fetchall(self):
        # import gc
        # gc.collect()

        # 有fetchall
        rs = db_session.execute(self.select_sql)
        db_session.commit()

        start = time.time()
        rs = rs.fetchall()
        hav_ids = [str(id_) for (id_, _, _, _, _, _) in rs] if rs else []
        hav_fetchall = time.time() - start

        # 无fetchall
        rp = db_session.execute(self.select_sql)
        db_session.commit()

        start = time.time()
        non_ids = [str(id_) for (id_, _, _, _, _, _) in rp] if rp else []
        non_fetchall = time.time() - start

        # import pdb
        # pdb.set_trace()

        rs_size = sys.getsizeof(rs)
        rp_size = sys.getsizeof(rp)

        print("Rs Size: %s" % rs_size)
        print("Rp Size: %s" % rp_size)

        print("Hav_Fetchall: %s" % hav_fetchall)
        print("Non_Fetchall: %s" % non_fetchall)
        print("Hav: %s Non: %s" % (len(hav_ids), len(non_ids)))

        # 去掉Fetchall性能上能不能带来改进?
        # 去掉Fetchall性能带不上改进, 反而适得其反.

        # 内存
        assert rs_size <= rp_size
        # 时间
        assert non_fetchall <= hav_fetchall
