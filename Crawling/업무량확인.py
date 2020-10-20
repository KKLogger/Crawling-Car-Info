from typing import no_type_check_decorator
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests as req
from urllib.parse import urlparse


def get_domain_list(urls):
    result = list()
    for url in urls:
        url_parse = urlparse(url)
        result.append(url_parse.netloc)
    result = list(set(result))
    return result

    # urls = pd.read_csv('C:/Users/jlee/Crawling-Car-Info/urls.csv')
urls = pd.read_csv('./urls.csv')
urls = urls['url'].values
chk_tag_urls = list()
total_url = len(urls)
current_url = 0
img_cnt = 0
iframe_cnt = 0
other_page_cnt = 0
no_data_cnt = 0
for url in urls:
    current_url += 1
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.kbchachacha.com',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    res = req.get(
        url, headers=headers)
    soup = bs(res.text, 'lxml')
    chk_tag_url = soup.find('li', {'class': 'used01'}).find('a')[
        'data-link-url']
    chk_tag_urls.append(chk_tag_url)

    # 개수 확인

    if 'http' in chk_tag_url:  # 다른 페이지로 이동
        # call domain by scraper
        other_page_cnt += 1
        pass
    else:
        print(url)
        carSeq = url[url.index('?carSeq=')+len('?carSeq='):]
        data = {
            'layerId': 'layerCarCheckInfo',
            'carSeq': carSeq
        }
        res = req.post(
            'https://www.kbchachacha.com/public/layer/car/check/info.kbc', data=data)

        soup = bs(res.text, 'lxml')

        img_check = soup.find('div', {'class': 'ch-car-txt'})
        if img_check == None:
            if soup.find('div', {'class': 'ch-car-name'}) == None:
                print("None Data")
                no_data_cnt += 1
            else:
                # call iframe scraper
                print("iframe")
                iframe_cnt += 1
        else:
            print("image")
            img_cnt += 1
    print(current_url, "/////", total_url)
    print("=============================================================================================================")
    print("총 개수", total_url, "이미지 개수", str(img_cnt),
          "kb차차차페이지", str(iframe_cnt), " 다른페이지연결 ", str(other_page_cnt), "점검기록이 없는 차 ", str(no_data_cnt))
