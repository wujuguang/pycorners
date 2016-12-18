# !/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

from unittest import TestCase
from conf import debug, db_session
from table import FollowUP


class BaseTestCase(TestCase):
    def setUp(self):
        # 填充测试数据.
        insert_sql = (
            "INSERT INTO `followup`(`category`,`codex`,`content`,`staff_id`,"
            "`student_id`,`type`,`next_contact_time`) "
            "VALUES(1,123,'hello,word',1,1,1,45534254)")

        for _ in range(0, 100):
            db_session.execute(insert_sql)

        db_session.commit()

    def tearDown(self):
        db_session.execute('drop table followup')
        db_session.execute('alter table followup_bck rename to followup')
        db_session.execute('truncate table followup')
        db_session.execute('truncate table table_division')
        db_session.commit()

    @staticmethod
    def test_followup():
        followup = FollowUP('followup', db_session, debug=debug)

        # 分表的配置数据置前设置.
        followup.table_capacity = 30
        followup.union_number = 0

        followup.run()
        print(followup.table_suffix)
        assert followup.table_suffix == 4
        followup.drop_table()
