# -*- coding: utf-8 -*-
import scrapy
import datetime
import MySQLdb
import json
from betting.items import BetcrisItem

class BetcrisSpider(scrapy.Spider):
    name = 'betcris'
    
    db = MySQLdb.connect(host="localhost",user="root",passwd="Callthelaw77",db="betcris")
    custom_settings = {
        'ITEM_PIPELINES': {
            'betting.pipelines.BetcrisPipeline':100
        }
    }
    allowed_domains = ['betcris.com']
    start_urls = ['https://www.betcris.com/en/sportsbook']
    body = ''
    teamsItem = []
    
    def getDate(self):
	    body = self.body
	    string = body.css('ul.tabbedMenu li.selected div.tab strong::text').extract_first()
	    string = string.replace("Bets", "")
	    string = string.encode('ascii','ignore')
	    string = string.replace('\n', '').replace('\r', '').strip()	    
	    return string
    
    def cleanText(self,text):
        if text:
            textFormatted = text.replace('\n', '').replace('\r', '').strip()
            return textFormatted
        else:
            return ''
    

    def processSports(self,sports):
        bc_date = self.getDate()
        a = 0
        for sport in sports:
		    bc_sport_name = sport.css('h1::text').extract_first()

		    leagues = sport.css('.league')
		    for league in leagues:
	    		bc_league_name = league.css('h2 a span::text').extract_first()
	    		
	    		
	    		if ("FUTURE" not in bc_league_name) and ("FUTURES" not in bc_league_name) and ("SPECIAL" not in bc_league_name) and ("GOLF PICK WINNER" not in bc_league_name):
	    		    externalLinesPages = league.css('.externalLinesPage')
    	    		for externalLinesPage in externalLinesPages:
    	    		    
    	    		    infoGame = externalLinesPage.css('.linesSubhead')
    	    		    matchups = externalLinesPage.css('.matchup')
    	   
    	    		    i = 1
    	    		    currentInfoGame = ''
    	    		    for matchup in matchups:
    	    		        
    	    		        
    	    		        time = matchup.css('li.time span::text').extract_first('')
    	    		        bc_time = self.cleanText(time)

    	    		        
    	    		        bc_v_team_name = matchup.css('.odds .vTeam .team h3 span::text').extract_first(default='-')
    	    		        bc_v_spread = matchup.css('.odds .vTeam .spread a span span::text').extract_first(default='-')
    	    		        bc_v_total = matchup.css('.odds .vTeam .total a span span::text').extract_first(default='-')
    	    		        bc_v_money = matchup.css('.odds .vTeam .money a span span::text').extract_first(default='-')
    	    		        
    	    		        bc_h_team_name = matchup.css('.odds .hTeam .team h3 span::text').extract_first()
    	    		        bc_h_spread = matchup.css('.odds .hTeam .spread a span span::text').extract_first(default='-')
    	    		        bc_h_total = matchup.css('.odds .hTeam .total a span span::text').extract_first(default='-')
    	    		        bc_h_money = matchup.css('.odds .hTeam .money a span span::text').extract_first(default='-')
    	    		        
    	    		        bc_d_spread = matchup.css('.odds .dTeam .spread a span::text').extract_first(default='-')
    	    		        bc_d_total = matchup.css('.odds .dTeam .total a span::text').extract_first(default='-')
    	    		        bc_d_money = matchup.css('.odds .dTeam .money a span::text').extract_first(default='-')
    	    		        print "bc_d_money: "+bc_d_money
    	    		        
    	    		        # Guess info game
    	    		        tmpInfoGame = infoGame[i].css('.linesSubhead span::text').extract_first(default='-')
    	    		        if tmpInfoGame:
    	    		            currentInfoGame = tmpInfoGame
    	    		         
    	    		        if i == 1 and currentInfoGame == '':
    	    		            currentInfoGame = infoGame[0].css('.linesSubhead span::text').extract_first(default='-')
    	    		            
    	    		        bc_info_game = currentInfoGame
    	    	
                            
    	    		        # Format date for MySQL DATETIME
    	    		        if bc_time:
    	    		            dateTmp = bc_date+" "+bc_time
    	    		            datetime_object = datetime.datetime.strptime(dateTmp, '%A, %B %d, %Y %I:%M %p')
    	    		        else:
    	    		            dateTmp = bc_date
    	    		            datetime_object = datetime.datetime.strptime(dateTmp, '%A, %B %d, %Y')
    	    		        
    	    		        
    	    		        itemBetObj = BetcrisItem()
    	    		        itemBetObj['league_name'] = bc_league_name
    	    		        itemBetObj['date'] = datetime_object
    	    		        itemBetObj['sport'] = bc_sport_name
    	    		        itemBetObj['info'] = bc_info_game
    	    		        itemBetObj['v_team_name'] = bc_v_team_name
    	    		        itemBetObj['h_team_name'] = bc_h_team_name
    	    		        itemBetObj['v_spread'] = bc_v_spread
    	    		        itemBetObj['v_total'] = bc_v_total
    	    		        itemBetObj['v_money'] = bc_v_money
    	    		        itemBetObj['h_spread'] = bc_h_spread
    	    		        itemBetObj['h_total'] = bc_h_total
    	    		        itemBetObj['h_money'] = bc_h_money
    	    		        itemBetObj['d_spread'] = bc_d_spread
    	    		        itemBetObj['d_total'] = bc_d_total
    	    		        itemBetObj['d_money'] = bc_d_money
    	    		        self.teamsItem.append(itemBetObj)
    	    		        
    	    		        print itemBetObj
                            
                            i = i+1
	
	
    def parse(self, response):
	    self.body = response
	    
	    
	    sports = response.css('.gameSchedule div.sport')
	    self.processSports(sports)
	    return self.teamsItem
	    
                 

	    
	    pass
