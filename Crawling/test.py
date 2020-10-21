
import requests
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import json
from urllib.request import urlopen


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


def get_car_info(url):
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
    car_price = soup.find(
        'div', {'class': 'car-buy-price'}).find('div').find('strong').text
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
    temp.append(car_price)
    temp = temp+car_info
    temp.append(url)
    temp.append(dealer_name)
    temp.append(dealer_location)
    temp.append(dealer_phone)

    columns = ['브랜드', '차량이름', '트림', '차량가격', '차량번호', '연식', '주행거리', '연료', '변속기', '연비', '차종', '배기량', '색상', '세금미납',
               '압류', '저당', '제시번호', '전속이력', '침수이력', '용도이력', '소유자변경', 'url', '딜러이름', '딜러위치', '딜러전화번호']
    df = pd.DataFrame([temp], columns=columns)
    result = df_to_dict(df)
    return result


def get_options(url):
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
    result = dict()
    result_t = dict()
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
    columns = ['선루프', '제논라이트(HID)', '알루미늄휠', '전동접이식미러',
               '주간주행등(DLR)', '파노라마썬루프', '루프랙', 'LED리어램프', '하이빔 어시스트', '고스트 도어 클로징', '자동슬라이딩도어', '전동사이드스탭',
               '어댑티드헤드램프', '열선시트', '통풍시트', '파워핸들', '핸들 리모컨', '가죽시트', '운전석전동시트', '조수석전동시트', '뒷좌석전동시트', '메모리시트', '안마시트', '슈퍼비전계기판', '패들시프트', '하이패스',
               '메모리시트(동승석)', '열선시트(뒷좌석)', '엠비언트라이트', '워크인시트', '전동햇빛가리개', '통풍시트(동승석)', '통풍시트(뒷좌석)', '후방감지센서', '사이드&커튼에어백', '운전석에어백', '조수석에어백', '후방카메라',
               '어라운드뷰', '블랙박스', 'ABS', 'ECS', 'TCS', '차체자세제어장치', '차선이탈경보장치', '도난경보기', '타이어 공기압감지', '무릎에어백', '주차감지센서(전방)', '전방카메라', '자동긴급제동(AEB)', '스마트키', '파워윈도우', '자동도어잠금', '풀오토에어컨', '오토라이트', '자동주차시스템',
               '전자식파킹브레이크', 'HUD', 'ECM룸밀러', '크루즈컨트롤', '전동트렁크', '핸들열선', '무선도어 잠금장치', '레인센서와이퍼', '스탑앤고', '무선충전', '내비게이션', 'CD플레이어', 'CD체인저', 'AV시스템', 'MP3', 'AUX', 'USB', '핸즈프리', 'iPod 단자', '뒷좌석모니터', '스마트폰미러링', '내비게이션 (비순정)', '블루투스']
    df = pd.DataFrame([temp], columns=columns)
    result = df_to_dict(df)
    return result


def df_to_dict(df):
    result = df.to_dict()
    for key, value in result.items():
        result[key] = list(value.values())[0]
    return result


def get_history(url):

    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    soup = str(soup)
    str_len = len('carHistorySeq = "')
    carHistorySeq = soup[soup.index(
        'carHistorySeq = "')+str_len:soup.index('"', soup.index('carHistorySeq = "')+str_len)]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '50',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.kbchachacha.com',
        'Origin': 'https://www.kbchachacha.com',
        'Referer': url,
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    }
    datas = {
        'layerId': 'layerCarHistoryInfo',
        'carHistorySeq': carHistorySeq
    }
    response = requests.post(
        'https://www.kbchachacha.com/public/layer/car/history/info.kbc', headers=headers, data=datas)
    soup = bs(response.text, 'lxml')
    hide_list = soup.find('ul', {'class': 'hide-list'}
                          ).find_all('span', {'class': 'txt'})
    registeredDate = soup.find('div', {'class': 'b-right'}).find_all('tr')
    registeredDate = registeredDate[3].find('td').text.strip()
    noRegisterPeriod = soup.find('div', {'class', 'box-line'})
    if noRegisterPeriod.find('div', {'class', 'date'}) is None:
        noRegisterPeriod = "None"
    else:
        noRegisterPeriod = noRegisterPeriod.find('div', {'class', 'date'}).text
    result = dict()
    result['전손 보험사고'] = hide_list[0].text.strip()
    result['도난 보험사고'] = hide_list[1].text.strip()
    result['침수 보험사고'] = hide_list[2].text.strip()
    result['특수 용도 이력'] = hide_list[3].text.strip()
    result['내차 피해'] = hide_list[4].text.strip()
    result['상대차 피해'] = hide_list[5].text.strip()
    result['소유자 변경'] = hide_list[6].text.strip()
    result['차량번호 변경'] = hide_list[7].text.strip()
    result['최초보험등록날짜'] = registeredDate
    result['미가입기간'] = noRegisterPeriod

    return result

    # main


def start():
    result = list()
    car_urls = get_car_urls()
    # df = pd.DataFrame()
    # df['url'] = car_urls
    # print(df.head)
    # df.to_csv('urls.csv', sep=',', encoding='euc-kr')
    # print(len(car_urls))
    num = 0
    for url in car_urls:
        print(url)
        num += 1
        print(len(car_urls), "중에", num)
        temp = dict()
        temp = get_car_info(
            url)
        temp['사고이력조회'] = get_history(
            url)

        temp['옵션내역'] = get_options(
            url)
        temp['성능점검'] = get_checkdata(url)
        result.append(temp)

    with open('./result.json', 'w', encoding='utf-8-sig') as outfile:
        json.dump(result, outfile, indent=4,
                  ensure_ascii=False, sort_keys=True)

    # dict = {'안':'녕'}
    # with open ('j.json', 'w',encoding='utf-8-sig') as file:
    #     file.write(json.dumps(dict,ensure_ascii=False))
    print("완-----료")


def crawl_iframe(url):
    result = dict()
    carSeq = url[url.index('?carSeq=') + len('?carSeq='):]
    data = {
        'layerId': 'layerCarCheckInfo',
        'carSeq': carSeq
    }
    res = requests.post(
        'https://www.kbchachacha.com/public/layer/car/check/info.kbc', data=data)
    soup = bs(res.text, 'lxml')

    result = dict()
    table = soup.find_all('table')
    result['변속기 종류'] = table[0].find_all('tr')[6].find('div').get('value')
    result['사용연료'] = table[0].find_all('tr')[7].find('div').get('value')
    result['원동기형식'] = table[0].find_all('tr')[8].find('td').text
    result['보증유형'] = table[0].find_all('tr')[9].find('div').get('value')
    result['가격잔정 기준가격'] = table[0].find_all('tr')[10].find('td').text.strip()
    result['주행거리 계기상태'] = table[1].find('tbody').find_all(
        'tr')[0].find('div', {'class': 'option-ch'}).get('value')
    result['주행거리 상태'] = table[1].find('tbody').find_all(
        'tr')[1].find('div', {'class': 'option-ch'}).get('value')
    result['현재 주행거리'] = table[1].find('tbody').find_all(
        'tr')[0].find('td', {'rowspan': '2'}).text
    result['차대번호 표기'] = table[1].find('tbody').find_all(
        'tr')[2].find('div', {'class': 'option-ch'}).get('value')
    result['배출가스'] = table[1].find('tbody').find_all(
        'tr')[3].find('div', {'class': 'option-ch'}).get('value')
    result['튜닝'] = table[1].find('tbody').find_all(
        'tr')[4].find('div', {'class': 'option-ch'}).get('value')
    result['사고이력'] = table[2].find('tbody').find_all('tr')[0].find_all(
        'div', {'class': 'option-ch'})[0].get('value')
    result['단순수리이력'] = table[2].find('tbody').find_all(
        'tr')[0].find_all('div', {'class': 'option-ch'})[1].get('value')
    result['외판부위 1랭크 이상여부'] = table[2].find('tbody').find_all(
        'tr')[1].find('div', {'class': 'option-ch'}).get('value')
    result['외판부위 2랭크 이상여부'] = table[2].find('tbody').find_all(
        'tr')[2].find('div', {'class': 'option-ch'}).get('value')
    result['주요골격 이상여부'] = table[2].find('tbody').find_all(
        'tr')[3].find('div', {'class': 'option-ch'}).get('value')
    result['자가진단 원동기'] = table[4].find('tbody').find_all(
        'tr')[0].find('div', {'class': 'option-ch'}).get('value')
    result['자가진단 변속기'] = table[4].find('tbody').find_all(
        'tr')[1].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 작동상태(공회전)'] = table[4].find('tbody').find_all(
        'tr')[2].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 오일누유 실린더커버'] = table[4].find('tbody').find_all(
        'tr')[3].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 실린더헤드/개스킷'] = table[4].find('tbody').find_all(
        'tr')[4].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 실린더블록/오일팬'] = table[4].find('tbody').find_all(
        'tr')[5].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 오일 유량및 오염'] = table[4].find('tbody').find_all(
        'tr')[6].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 냉각수누수 실린더헤드/개스킷'] = table[4].find('tbody').find_all(
        'tr')[7].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 냉각수누수 워어펌프'] = table[4].find('tbody').find_all(
        'tr')[8].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 냉각수누수 라디에이터'] = table[4].find('tbody').find_all(
        'tr')[9].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 냉각수누수 냉각수 수량'] = table[4].find('tbody').find_all(
        'tr')[10].find('div', {'class': 'option-ch'}).get('value')
    result['원동기 고압펌프-디젤엔진'] = table[4].find('tbody').find_all(
        'tr')[11].find('div', {'class': 'option-ch'}).get('value')
    result['자동변속기 오일누유'] = table[4].find('tbody').find_all(
        'tr')[12].find('div', {'class': 'option-ch'}).get('value')
    result['자동변속기 오일유량및상세'] = table[4].find('tbody').find_all(
        'tr')[13].find('div', {'class': 'option-ch'}).get('value')
    result['자동변속기 작동상태(공회전)'] = table[4].find('tbody').find_all(
        'tr')[14].find('div', {'class': 'option-ch'}).get('value')
    result['수동변속기 오일누유'] = table[4].find('tbody').find_all(
        'tr')[15].find('div', {'class': 'option-ch'}).get('value')
    result['수동변속기 기어변속장치'] = table[4].find('tbody').find_all(
        'tr')[16].find('div', {'class': 'option-ch'}).get('value')
    result['수동변속기 오일유량및상태'] = table[4].find('tbody').find_all(
        'tr')[17].find('div', {'class': 'option-ch'}).get('value')
    result['수동변속기 작동상태(공회전)'] = table[4].find('tbody').find_all(
        'tr')[18].find('div', {'class': 'option-ch'}).get('value')
    result['동력전달 클러치어셈블러'] = table[4].find('tbody').find_all(
        'tr')[19].find('div', {'class': 'option-ch'}).get('value')
    result['동력전달 등속조인트'] = table[4].find('tbody').find_all(
        'tr')[20].find('div', {'class': 'option-ch'}).get('value')
    result['동력전달 추진축및베어링'] = table[4].find('tbody').find_all(
        'tr')[21].find('div', {'class': 'option-ch'}).get('value')
    result['동력전달 디퍼렌셜기어'] = table[4].find('tbody').find_all(
        'tr')[22].find('div', {'class': 'option-ch'}).get('value')
    result['조향 동력조향작동오일노유'] = table[4].find('tbody').find_all(
        'tr')[23].find('div', {'class': 'option-ch'}).get('value')
    result['조향 작동상태 스티어링펌프'] = table[4].find('tbody').find_all(
        'tr')[24].find('div', {'class': 'option-ch'}).get('value')
    result['조향 작동상태 스티어링기어'] = table[4].find('tbody').find_all(
        'tr')[25].find('div', {'class': 'option-ch'}).get('value')
    result['조향 작동상태 스티어링조인트'] = table[4].find('tbody').find_all(
        'tr')[26].find('div', {'class': 'option-ch'}).get('value')
    result['조향 작동상태 파워고압호스'] = table[4].find('tbody').find_all(
        'tr')[27].find('div', {'class': 'option-ch'}).get('value')
    result['조향 작동상태 타이로드엔드및볼조인트'] = table[4].find('tbody').find_all(
        'tr')[28].find('div', {'class': 'option-ch'}).get('value')
    result['제동 브레이크마스터실린더오일누유'] = table[4].find('tbody').find_all(
        'tr')[29].find('div', {'class': 'option-ch'}).get('value')
    result['제동 브레이크오일누유'] = table[4].find('tbody').find_all(
        'tr')[30].find('div', {'class': 'option-ch'}).get('value')
    result['제동 배력장치상태'] = table[4].find('tbody').find_all(
        'tr')[31].find('div', {'class': 'option-ch'}).get('value')
    result['전기 발전기출력'] = table[4].find('tbody').find_all(
        'tr')[32].find('div', {'class': 'option-ch'}).get('value')
    result['전기 시동모터'] = table[4].find('tbody').find_all(
        'tr')[33].find('div', {'class': 'option-ch'}).get('value')
    result['전기 와이퍼모터기능'] = table[4].find('tbody').find_all(
        'tr')[34].find('div', {'class': 'option-ch'}).get('value')
    result['전기 실내송풍모터'] = table[4].find('tbody').find_all(
        'tr')[35].find('div', {'class': 'option-ch'}).get('value')
    result['전기 라디에이터팬모터'] = table[4].find('tbody').find_all(
        'tr')[36].find('div', {'class': 'option-ch'}).get('value')
    result['전기 윈도우모터작동'] = table[4].find('tbody').find_all(
        'tr')[37].find('div', {'class': 'option-ch'}).get('value')
    result['고전원전기장치 충전구절연상태'] = table[4].find('tbody').find_all(
        'tr')[38].find('div', {'class': 'option-ch'}).get('value')
    result['고전원전기장치 구동축전지격리상태'] = table[4].find('tbody').find_all(
        'tr')[39].find('div', {'class': 'option-ch'}).get('value')
    result['고전원전기장치 고전원전기배선상태'] = table[4].find('tbody').find_all(
        'tr')[40].find('div', {'class': 'option-ch'}).get('value')
    result['연료 연료누출'] = table[4].find('tbody').find_all(
        'tr')[41].find('div', {'class': 'option-ch'}).get('value')
    # result['수리필요 외장'] = table[5].find('tbody').find_all(
    #     'tr')[0].find('div', {'class': 'option-ch'}).get('value')
    # result['수리필요 광택'] = table[5].find('tbody').find_all(
    #     'tr')[1].find('div', {'class': 'option-ch'}).get('value')
    # result['수리필요 내장'] = table[5].find('tbody').find_all(
    #     'tr')[2].find('div', {'class': 'option-ch'}).get('value')
    # result['수리필요 룸크리닝'] = table[5].find('tbody').find_all(
    #     'tr')[3].find('div', {'class': 'option-ch'}).get('value')
    # result['수리필요 휠'] = table[5].find('tbody').find_all(
    #     'tr')[4].find('div', {'class': 'option-ch'}).get('value')
    # result['수리필요 타이어'] = table[5].find('tbody').find_all(
    #     'tr')[5].find('div', {'class': 'option-ch'}).get('value')
    # result['수리필요 유리'] = table[5].find('tbody').find_all(
    #     'tr')[6].find('div', {'class': 'option-ch'}).get('value')
    # result['기본품목 보유상태'] = table[5].find('tbody').find_all(
    #     'tr')[7].find('div', {'class': 'option-ch'}).get('value')
    result['성능점검일'] = soup.find('div', {'class': 'date'}).text

    return result


def get_checkdata(url):
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
    res = requests.get(
        url, headers=headers)
    soup = bs(res.text, 'lxml')
    chk_tag_url = soup.find('li', {'class': 'used01'}).find('a')[
        'data-link-url']
    if 'http' in chk_tag_url:  # 다른 페이지로 이동
        # call domain by scraper
        result = "other page"
    else:
        carSeq = url[url.index('?carSeq=')+len('?carSeq='):]
        data = {
            'layerId': 'layerCarCheckInfo',
            'carSeq': carSeq
        }
        res = requests.post(
            'https://www.kbchachacha.com/public/layer/car/check/info.kbc', data=data)

        soup = bs(res.text, 'lxml')

        img_check = soup.find('div', {'class': 'ch-car-txt'})
        if img_check == None:
            if soup.find('div', {'class': 'ch-car-name'}) == None:
                result = "no data"
                # print("None Data")
                pass
            else:

                # call iframe scraper
                result = crawl_iframe(url)
        else:
            # print("image")
            get_image(url)
            result = "image"

    return result

    # 성능점검 url 구하기
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


def get_image(url):
    carSeq = url[url.index('?carSeq=') + len('?carSeq='):]
    data = {
        'layerId': 'layerCarCheckInfo',
        'carSeq': carSeq
    }
    res = requests.post(
        'https://www.kbchachacha.com/public/layer/car/check/info.kbc', data=data)
    soup = bs(res.text, 'lxml')
    title = soup.find('h2').text.split(' ')[1]
    img_urls = soup.find_all('img')
    img_urls = [x.get('src') for x in img_urls]
    for num, img_url in enumerate(img_urls):
        with urlopen(img_url) as f:
            with open('image/' + str(num) + title + '.jpg', 'wb') as h:
                img = f.read()
                h.write(img)


start()
