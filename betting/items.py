# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class BettingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
    
class BetcrisItem(scrapy.Item):
    # define the fields for your item here like:
    league_name = scrapy.Field()
    sport = scrapy.Field()
    date = scrapy.Field()
    info = scrapy.Field()
    v_team_name = scrapy.Field()
    h_team_name = scrapy.Field()
    v_spread = scrapy.Field()
    v_total = scrapy.Field()
    v_money = scrapy.Field()
    h_spread = scrapy.Field()
    h_total = scrapy.Field()
    h_money = scrapy.Field()
    d_spread = scrapy.Field()
    d_total = scrapy.Field()
    d_money = scrapy.Field()
    
    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()