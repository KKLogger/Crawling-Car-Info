import requests
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool, freeze_support, Manager
import pandas as pd

manager = Manager()
car_url_list = manager.list()


def get_page_url(page_num, user_code):
    url = 'https://www.kbchachacha.com/public/search/list.empty?page=' + \
        str(page_num) + '&sort=-orderDate&useCode=' + \
        str(user_code) + '&_pageSize=3&pageSize=4'
    return url


def get_car_urls(user_codes):

    for user_code in user_codes:
        page_num = 0
        while(True):
            page_num += 1
            url = get_page_url(page_num, user_code)
            print(url)
            response = requests.get(url)
            soup = bs(response.text, "html.parser")
            print(page_num)
            ######종료 조건 ###############
            if page_num == 3:
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
                            'https://www.kbchachacha.com' + item_href)

    # return car_url_list


def main():
    user_codes = ['002001', '002002', '002003', '002004', '002005', '002006',
                  '002007', '002008', '002009', '002010', '002011', '002012', '002013']
    pool = Pool(processes=4)
    pool.map(get_car_urls, ['002001', '002002', '002003', '002004', '002005', '002006',
                            '002007', '002008', '002009', '002010', '002011', '002012', '002013'])
    print(len(car_url_list))
    df = pd.DataFrame({'filtered_url': car_url_list})
    df.to_csv('filtered_url.csv')


if __name__ == '__main__':
    freeze_support()
    pool = Pool(processes=4)
    pool.map(get_car_urls, ['002001', '002002', '002003', '002004', '002005', '002006',
                            '002007', '002008', '002009', '002010', '002011', '002012', '002013'])
