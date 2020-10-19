import pandas as pd
import os

path = "C:/Users/jlee/Crawling-Car-Info/Crawling/carInfo/carInfo/성능점검urls.csv"
df = pd.read_csv(path, encoding='euc-kr')

domains = list()

for domain in df['1']:
    if 'http' in domain:
        domains.append(domain)
domains = list(set(domains))


print(len(domains))
