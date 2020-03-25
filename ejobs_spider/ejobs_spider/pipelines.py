# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
import MySQLdb


class EjobsSpiderPipeline(object):
    def __init__(self):
        self.connection = MySQLdb.connect('localhost', 'root', 'parola123', 'ejobs')
        self.cursor = self.connection.cursor()
        
        self.connection.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')


    def process_item(self, item, spider):
        self.cursor.execute("""
        INSERT INTO jobs (
            id,
            jname,
            company,
            jdate
            )
            VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
            jname = VALUES(jname),
            company = VALUES(company),
            jdate = VALUES(jdate)
            """,
        (
            item['id'],
            item['jname'],
            item['company'],
            item['jdate']
        ))
        self.connection.commit()