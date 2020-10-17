
import requests
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import json


def get_page_url(page_num):
    url = 'https://www.kbchachacha.com/public/search/list.empty?page=' + \
        str(page_num) + '&sort=-orderDate&makerCode=101&_pageSize=3&pageSize=4'
    return url


def get_car_urls():

    car_url_list = list()
    page_num = 0
    while(True):
        page_num += 1
        url = get_page_url(page_num)
        print(url)
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        print(page_num)
        #########종료 조건 ###############
        if page_num == 5:
            break
        # if soup.find('span', {'class': 'txt'}) is not None:
        #     print('종료')
        #     break

        items = soup.find_all('a')
        for item in items:
            if 'detail.kbc?carSeq' in item['href']:
                item_href = item['href']
                if 'https://' in item_href:
                    car_url_list.append(item_href)
                else:
                    car_url_list.append(
                        'https://www.kbchachacha.com/' + item_href)

    car_url_list = list(set(car_url_list))
    return car_url_list


def get_car_info(urls):
    result = []
    car_dict = dict()
    for url in urls:
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
        response = requests.get(url, headers=headers)
        print(url)
        print(response)
        soup = bs(response.text, 'html.parser')

        car_b_n_t = soup.find('strong', {'class': 'car-buy-name'})
        car_b_n = str(car_b_n_t).split('<br/>')[0]
        car_b_n = car_b_n[car_b_n.index(')')+1:]
        car_brand = car_b_n[:car_b_n.index(' ')]
        car_name = car_b_n[car_b_n.index(' ')+1:]
        car_trim = str(car_b_n_t).split('<br/>')[1]
        car_trim = car_trim[:car_trim.index('<')].strip()

        car_info1 = soup.find('dl', {'class': 'claerFix'}).find_all('dd')
        car_info1 = [x.text.strip().replace(' ', '') for x in car_info1]

        car_info2 = soup.find('div', {'class': 'detail-info02'}).find_all('dd')
        car_info2 = [x.text.strip().replace(' ', '') for x in car_info2]

        car_info = car_info1 + car_info2

        # dealer 정보
        dealer_info = soup.find('div', {'class': 'dealer-cnt'})
        dealer_name = dealer_info.find('span', {'class', 'name'}).text.strip()
        dealer_location = dealer_info.find(
            'span', {'class', 'place-add'}).text.strip()
        dealer_phone = dealer_info.find(
            'div', {'class': 'dealer-tel-num'}).text.strip()
        temp = list()
        temp.append(car_brand)
        temp.append(car_name)
        temp.append(car_trim)
        temp = temp+car_info
        temp.append(dealer_name)
        temp.append(dealer_location)
        temp.append(dealer_phone)
        temp.append(url)
        result.append(temp)

    return result


def get_detail_info(urls):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '42',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.kbchachacha.com',
        'Origin': 'https://www.kbchachacha.com',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    jump = len('?carSeq=')
    result = list()
    for url in urls:
        index = url.index('?carSeq=') + jump
        carSeq = url[index:]
        data = {
            'layerId': 'layerCarOptionView',
            'carSeq': carSeq
        }
        res = requests.post(
            'https://www.kbchachacha.com/public/layer/car/option/list.kbc', headers=headers, data=data)
        soup = bs(res.text, 'lxml')
        option_codes = soup.find('input', {'id': 'carOption'})[
            'value'].split(',')
        res = requests.post(
            'https://www.kbchachacha.com/public/car/option/code/list.json')
        json_datas = json.loads(res.text)
        json_datas = json_datas['optionList']
        all_option_codes = list()
        for json_data in json_datas:
            all_option_codes.append(json_data['optionCode'])
        temp = list()
        for code in all_option_codes:
            if code in option_codes:
                temp.append('1')
            else:
                temp.append('0')
        result.append(temp)
    return result

# main


def start():
    car_urls = get_car_urls()
    result = get_car_info(car_urls)
    columns = ['브랜드', '차량이름', '트림', '차량번호', '연식', '주행거리', '연료', '변속기', '연비', '차종', '배기량', '색상', '세금미납',
               '압류', '저당', '제시번호', '전속이력', '침수이력', '용도이력', '소유자변경', '딜러이름', '딜러위치', '딜러전화번호', 'url']
    df = pd.DataFrame(result, columns=columns)

    add_col = ['선루프', '제논라이트(HID)', '알루미늄휠', '전동접이식미러',
               '주간주행등(DLR)', '파노라마썬루프', '루프랙', 'LED리어램프', '하이빔 어시스트']
    add_col = add_col + ['고스트 도어 클로징', '자동슬라이딩도어', '전동사이드스탭',
                         '어댑티드헤드램프', '열선시트', '통풍시트', '파워핸들', '핸들 리모컨', '가죽시트', '운전석전동시트']
    add_col = add_col + ['조수석전동시트', '뒷좌석전동시트', '메모리시트', '안마시트', '슈퍼비전계기판', '패들시프트', '하이패스',
                         '메모리시트(동승석)', '열선시트(뒷좌석)', '엠비언트라이트', '워크인시트', '전동햇빛가리개', '통풍시트(동승석)', '통풍시트(뒷좌석)', '후방감지센서', '사이드&커튼에어백', '운전석에어백', '조수석에어백', '후방카메라', ]

    add_col = add_col + ['어라운드뷰', '블랙박스', 'ABS', 'ECS', 'TCS', '차체자세제어장치', '차선이탈경보장치', '도난경보기', '타이어 공기압감지', '무릎에어백', '주차감지센서(전방)', '전방카메라', '자동긴급제동(AEB)', '스마트키', '파워윈도우', '자동도어잠금', '풀오토에어컨', '오토라이트', '자동주차시스템',
                         '전자식파킹브레이크', 'HUD', 'ECM룸밀러', '크루즈컨트롤', '전동트렁크', '핸들열선', '무선도어 잠금장치', '레인센서와이퍼', '스탑앤고', '무선충전', '내비게이션', 'CD플레이어', 'CD체인저', 'AV시스템', 'MP3', 'AUX', 'USB', '핸즈프리', 'iPod 단자', '뒷좌석모니터', '스마트폰미러링', '내비게이션 (비순정)', '블루투스']
    result = get_detail_info(car_urls)
    ad_df = pd.DataFrame(result, columns=add_col)

    result_df = pd.concat([df, ad_df], axis=1)
    result_df.to_csv('result.csv', sep=",", encoding='euc-kr', index=False)

#성능점검 url 구하기
# urls = get_car_urls()
# result = list()
# for url in urls:
#     print(url)
#     res = requests.get(url)
#     soup = bs(res.text, 'lxml')
#     perform_url_ele = soup.find('a', {'id': 'btnCarCheckView1'})
#     perform_url_ele = perform_url_ele['data-link-url']
#     if len(perform_url_ele) <= 2:
#         perform_url_ele = 'None'

#     print(perform_url_ele)
#     if '?' in perform_url_ele:
#         perform_domain_ele = perform_url_ele[:perform_url_ele.index('?')]
#     else:
#         perform_domain_ele = perform_url_ele
#     result.append([perform_url_ele, perform_domain_ele])
# df = pd.DataFrame(result)
# df.to_csv('성능점검urls.csv', sep=',', encoding='euc-kr', index=False)


start()
