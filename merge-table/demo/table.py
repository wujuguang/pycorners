# !/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function

from merge_table.base import TableSuffix


class FollowUP(TableSuffix):
    def work(self):
        create_table_sql = (
            'CREATE TABLE `followup{table_suffix}` ('
            '`id` int(12) unsigned NOT NULL AUTO_INCREMENT,'
            '`category` tinyint unsigned DEFAULT NULL,'
            '`codex` int(10) unsigned DEFAULT NULL,'
            '`content` varchar(255) NOT NULL,'
            '`staff_id` int(12) unsigned NOT NULL,'
            '`student_id` int(12) unsigned NOT NULL,'
            '`type` tinyint(1) unsigned NOT NULL,'
            '`next_contact_time` int(12) unsigned NOT NULL,'
            '`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,'
            '`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
            'ON UPDATE CURRENT_TIMESTAMP,'
            'PRIMARY KEY (`id`),'
            'KEY `idx_student_staff` (`student_id`, `staff_id`),'
            'KEY `idx_student_category` (`student_id`, `category`),'
            'KEY `idx_staff_category_create_time` (`staff_id`, `category`, '
            '`create_time`),KEY `idx_staff_category_next_contact_time` '
            '(`staff_id`, `category`, `next_contact_time`)'
            ') ')

        self.create_table_sql = create_table_sql
        return super(FollowUP, self).work()
