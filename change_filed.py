from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import json
import os


with open('C:/Users/jlee/Crawling-Car-Info/result.json', 'r', encoding='utf-8-sig') as json_file:
    json_datas = json.load(json_file)

result = list()
for json_data in json_datas:
    try:
        print(json_data['CarNumber'])
    except:
        del json_data
        print("error")
        continue
    json_data['Grade'] = json_data['세부모델']
    json_data['Badge'] = json_data['모델명']
    json_data['Model'] = json_data['차종']
    json_data['Manufacturer'] = json_data['브랜드']
    json_data['Year'] = json_data['연식']
    json_data['Price'] = json_data['가격']
    json_data['FuelType'] = json_data['연료']
    json_data['Displacement'] = json_data['배기량']
    json_data['Transmission'] = json_data['변속기']

    # ExtendWarranty 추가
    del json_data['세부모델']
    del json_data['모델명']
    del json_data['차종']
    del json_data['브랜드']
    del json_data['연식']
    del json_data['가격']
    del json_data['연료']
    del json_data['배기량']
    del json_data['변속기']
    result.append(json_data)
print(len(result))
with open('./result_ss.json', 'w', encoding='utf-8-sig') as outfile:
    json.dump(result, outfile, indent=4,
              ensure_ascii=False, sort_keys=True)
