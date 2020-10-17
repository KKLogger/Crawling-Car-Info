import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import time
import os


class CarInfoSpider(scrapy.Spider):
    name = 'car_info'

    def get_dynamic_html(self, url):
        driver = webdriver.Chrome('./chromedriver.exe')
        driver.get(url)
        time.sleep(2)
        html = str(driver.page_source)
        driver.quit()
        selector = Selector(text=html)
        return selector

    def get_page_url(page_num):
        url = 'https://www.kbchachacha.com/public/search/list.empty?page=' + \
            str(page_num) + '&sort=-orderDate&makerCode=101&_pageSize=3&pageSize=4'
        return url


    def start_requests(self):

        yield scrapy.Request(url=self.main_url+str(self.page_num), callback=self.get_maxnum)
