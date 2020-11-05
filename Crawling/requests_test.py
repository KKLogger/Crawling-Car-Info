import requests
from bs4 import BeautifulSoup as bs
url = "https://www.kbchachacha.com/public/search/list.empty?page=1&sort=-orderDate"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.kbchachacha.com',
    'Pragma': 'no-cache',
    'Cookie': 'WMONID=DIsAC5YxLe8; FIRST_APPROCH=y; _ga=GA1.2.89915624.1602553615; cha-cid=30c7e5e5-abc7-41bd-8d7f-bf0db71fc3b2; C_PC_LOGIN_TAB=031100; TR10062602448_t_pa1=3.0.0.132622.null.null.null.52525333192658139; TR10062602448_t_pa2=3.0.0.132622.null.null.null.52525333192658139; car-keyword-code=1011212277324445%3A6; _gid=GA1.2.1217362369.1604476473; recent-visited-car=20633536; page-no-action-count=5; JSESSIONID=iW2ZmuL0VQaQIiFbL4CJ9XiAgxYPpTMsbq6SiXGWmbE3j061VblYAaMU8NrJAM8X.cGNoYWFwbzFfZG9tYWluL0NBUjNBUF9zZXJ2ZXIyX2Nz; _gac_UA-78571735-4=1.1604578759.CjwKCAiA4o79BRBvEiwAjteoYJvnkHPDcj3Ta3kbmks3YndGqrgyYVHE4DQP0PQ3HzAAKsqB9f5i-hoCnS4QAvD_BwE; _gat_UA-78571735-4=1; TR10062602448_t_uid=49545853018139668.1604578760316; TR10062602448_t_sst=49545577600001139.1604578760316; TR10062602448_t_if=15.0.0.0.null.null.null.0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}
cookies = {

}
response = requests.get(url, headers=headers)
soup = bs(response.text, 'html.parser')
print(soup)
