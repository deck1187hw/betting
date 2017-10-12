# -*- coding: utf-8 -*-
import json
import base64
from scrapy.http import FormRequest

import scrapy
from scrapy_splash import SplashRequest




script = """
function main(splash)
	
	

    local bPlaced = 'no'
	local placeBetFlag = splash.args.placeBetFlag
	local money = splash.args.money
	
    splash.images_enabled = false
	assert(splash:go(splash.args.url))
	assert(splash:wait(3))
	
      
    local form = splash:select('#Form1')

    local values = assert(form:form_values())
    
    values.account = splash.args.username
    values.password = splash.args.password
    assert(form:fill(values))
    assert(form:submit())
    assert(splash:wait(0.1))
    assert(form:submit())
    assert(splash:wait(19))

    local get_elementByID = splash:jsfunc([[
	    
        function (IDElement) {
	        var rect = document.getElementById(IDElement).getClientRects()[0];
            return {"x": rect.left, "y": rect.top}
        }
    ]])
    
    local loadSchedule = splash:jsfunc([[
        function () {
            ProcessRequest('LoadSchedule','12068','scheduleLeague');
            console.log("Loading Schedule");
        }
    ]])
    
    local placeBets = splash:jsfunc([[
        function () {
            ProcessRequest('SetBets','1987463_12068_5_0_90404','scheduleLine');
            console.log("Loading screen for bet");            
        }
    ]])
    
    local placeBetEnd = splash:jsfunc([[
        function () {
            jQuery("#btnPlaceBet").removeAttr("disabled");
            jQuery("#btnPlaceBet").trigger("click");
        }
    ]])
    
    local checkSuccess = splash:jsfunc([[
        function () {
            var betPlaced = 'no';
            if ( jQuery( ".successMsg" ).length ) {
                betPlaced = 'yes';
            }
            return betPlaced;
        }
    ]])
    
    
    loadSchedule()
    assert(splash:wait(5))   
    
    placeBets()
    assert(splash:wait(6))
    
	
	local dimensions = get_elementByID('risk1987463_12068_5_0_90404')
    splash:mouse_click(dimensions.x, dimensions.y)
    assert(splash:wait(0.5))

	splash:send_keys(money)
    assert(splash:wait(2))
	

	if placeBetFlag=="1" then
      placeBetEnd()
	  assert(splash:wait(3.5))
    end


    bPlaced = checkSuccess()

    assert(splash:wait(1))

  return {
    betPlaced = bPlaced,
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""



class BetcrisBetSpider(scrapy.Spider):
    name = 'betcris_bet'
    allowed_domains = ['https://betcris.com']
    start_urls = ['https://be.betcris.com/en/loginpage']
    login_url = 'https://be.betcris.com/en/loginpage'

    def saveScreenshot(self,rawImage):
	    png_bytes = base64.b64decode(rawImage)
	    fh = open("/var/www/betcris/betting/betting/imageToSave.png", "wb")
	    fh.write(png_bytes)
	    fh.close()
    
    splash_args = {
            'html': 1,
            'png': 1,
            'money':'1',
            'console':1,
            'username':'CR103922',
            'password':'7TuTNVZK',
            'customTitle': 'miguelon',
            'placeBetFlag':'0',
            'width': 800,            
            'lua_source': script,
            'render_all': 1,
            'timeout':3600
        }
	
	
		
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_results,
	            endpoint='execute',
	            cache_args=['lua_source'],
	            args=self.splash_args,
	            headers={'X-My-Header': 'value'},
	        )

	
		
    def parse_results(self, response):

	    title = response.css('title').extract_first()
	    print title
	    #print response.data;
	    print "Bet placed: "+response.data['betPlaced']
	    print "Please check betcris.com and check the bets placed to confirm, also check the money left."
  
	    
	    #print response.data['html']
	    self.saveScreenshot(response.data['png'])

	    

	    pass
