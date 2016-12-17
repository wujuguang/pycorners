# !/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

import time

from conf import db_session
from table import FollowUP


def main():
    """
        包含两种逻辑, 自动判断是初次分表, 还是根据后续新增分表.
        每次新增分表后, 后续数据的写入到新增分表.

        部署方式可以加入supervisor或者screen里运行, 周期性地按指定时间间隔循环.
    """

    followup = FollowUP('followup', db_session)

    # 分表的配置数据置前设置.
    followup.table_capacity = 5
    followup.union_number = 0

    while True:
        has_data_total = followup.table_suffix * followup.table_capacity
        if followup.table_latest > has_data_total:
            followup.run()
        time.sleep(60 * 60)


def mirror():
    """
        包含两种逻辑, 自动判断是初次分表, 还是根据后续新增分表.
        每次新增分表后, 后续数据的写入到新增分表.

        部署方式可以加入到Cron里, 以数据的增量大致周期运行.
    """

    followup = FollowUP('followup', db_session)

    # 分表的配置数据置前设置.
    followup.table_capacity = 5
    followup.union_number = 0

    followup.run()
    # followup.drop_table()


if __name__ == '__main__':
    main()
    # mirror()
