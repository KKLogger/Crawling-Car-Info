import scrapy
from  selenium  import webdriver
from scrapy.selector import Selector
import time
import os
class CarInfoSpider(scrapy.Spider):
    name = 'car_info'
    start = 'https://www.kbchachacha.com/public/search/main.kbc'
    main_url = 'https://www.kbchachacha.com/public/search/main.kbc#!?page='
    page_num = 1
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,und;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'www.kbchachacha.com',
        'Referer': 'https://www.kbchachacha.com/?la_gc=TR10062602448&la_src=sa&la_cnfg=132622&gclid=CjwKCAjww5r8BRB6EiwArcckCwlL9pxg7ky-LUIIAMsKb_TPfQuUh3MZynxWSW-ilIwBoaw83lv5dBoC4g8QAvD_BwE',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
        }
    def get_dynamic_html(self, url):
        driver = webdriver.Chrome('./chromedriver.exe')
        driver.get(url)
        time.sleep(2)
        html = str(driver.page_source)
        driver.quit()
        selector = Selector(text=html)
        return selector

    def start_requests(self):
        
        yield scrapy.Request(url=self.main_url+str(self.page_num), callback=self.get_maxnum,headers=self.headers)
        
    def get_maxnum(self, response):
        print(response.url)
        print(self.page_num)
        if response.css('div.txt-box span.txt::text').get() == "죄송합니다":
            print(self.page_num)
        else :
            self.page_num = self.page_num + 1
            yield scrapy.Request(url=self.main_url+str(self.page_num), callback=self.get_maxnum,headers=self.headers)
               
            

        