import multiprocessing
from itertools import repeat
import requests
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool, freeze_support, Manager
import pandas as pd
import time

def get_page_url(page_num, user_code, maker_code):
    url = 'https://www.kbchachacha.com/public/search/list.empty?page=' + \
        str(page_num) + '&sort=-orderDate&useCode=' + \
        str(user_code) + '&makerCode=' + \
        str(maker_code)+'&_pageSize=3&pageSize=4'
    return url


def get_car_urls(user_code, car_url_list):
    maker_codes = ['101', '102', '103', '105',
                   '104', '189', '106', '107',
                   '108', '109', '112', '160',
                   '116', '122', '133', '115',
                   '110', '170', '153', '114',
                   '128', '123', '124', '117',
                   '136', '121', '137', '146',
                   '118', '142', '113', '138',
                   '130', '180', '166', '125',
                   '150', '148', '119', '156',
                   '129', '140', '111', '190',
                   '191', '132', '152', '161',
                   '157', '134', '181', '141',
                   '154', '126', '173', '139',
                   '169', '143', '167', '127']
    for maker_code in maker_codes:
        page_num = 0
        while(True):
            time.sleep(3)
            page_num += 1
            url = get_page_url(page_num, user_code, maker_code)
            print(url)
            response = requests.get(url)
            soup = bs(response.text, "html.parser")
            print(page_num)
            #####종료 조건 ###############
            # if page_num == 3:
            #     break
            if soup.find('span', {'class': 'txt'}) is not None:
                print('종료')
                break
            if soup.find('h2') is None:
                print('종료, blocked')
                break
            items = soup.find_all('a')
            for item in items:
                if 'detail.kbc?carSeq' in item['href']:
                    item_href = item['href']
                    if 'https://' in item_href:
                        car_url_list.append(item_href)
                    else:
                        car_url_list.append(
                            'https://www.kbchachacha.com' + item_href)

    # return car_url_list


if __name__ == '__main__':

    freeze_support()
    manager = Manager()
    car_url_list = manager.list()
    num_cores = multiprocessing.cpu_count()
    # https://dailyheumsi.tistory.com/105
    pool = Pool(processes=6)
    pool.starmap(get_car_urls, zip(['002001', '002002', '002003', '002004', '002005', '002006',
                                    '002007', '002008', '002009', '002010', '002011', '002012', '002013'], repeat(car_url_list)))
    pool.close()
    pool.join()
    df = pd.DataFrame(columns=['url'])
    car_url_list = list(set(car_url_list))
    df['url'] = car_url_list
    df.to_csv('filtered_url.csv')
    print(len(car_url_list))
