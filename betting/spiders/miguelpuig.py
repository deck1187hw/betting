# -*- coding: utf-8 -*-
import scrapy
import subprocess


class MiguelpuigSpider(scrapy.Spider):
    name = 'miguelpuig'
    allowed_domains = ['miguelpuig.com']
    start_urls = ['http://miguelpuig.com/']

    def parse(self, response):
	    print "hola! desde python"
