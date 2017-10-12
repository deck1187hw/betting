# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import MySQLdb

class BettingPipeline(object):
    def process_item(self, item, spider):
        return item


class BetcrisPipeline(object):


    def __init__(self):
        self.conn = MySQLdb.connect(
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DB'],
            host='localhost',
            charset="utf8",
            use_unicode=True
        )
        self.cursor = self.conn.cursor()
        self.cursor = self.conn.cursor()
        self.cursor.execute("""TRUNCATE TABLE games""")
        self.conn.commit()


    def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT games SET sport=%s,league_name=%s,date=%s,info=%s,v_team_name=%s,h_team_name=%s,v_spread=%s,v_total=%s,v_money=%s,h_spread=%s,h_total=%s,h_money=%s,d_spread=%s,d_total=%s,d_money=%s""", (item['sport'],item['league_name'],item['date'],item['info'],item['v_team_name'],item['h_team_name'],item['v_spread'],item['v_total'],item['v_money'],item['h_spread'],item['h_total'],item['h_money'],item['d_spread'],item['d_total'],item['d_money']))
			self.conn.commit()
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
		print "-------------- PROCESSING ITEM -----------"
		return item