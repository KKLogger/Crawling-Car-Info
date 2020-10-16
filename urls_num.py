import pandas as pd
import os

path ="C:/Users/koc08/바탕 화면/Crawling Car Info/carInfo/성능점검urls.csv"
df = pd.read_csv(path,encoding='euc-kr')

domains = list()

for domain in df['1']:
    if 'http' in domain:
        domains.append(domain)
domains = list(set(domains))


print(len(domains)) ## 65