import multiprocessing
import json
import pandas as pd
from ast import literal_eval


result = list()
with open('C:/Users/jlee/Crawling-Car-Info/Crawling/from_server/result21.json', encoding='utf-8-sig', errors='ignore') as f:
    str_data = f.read()
str_data = str(str_data)
str_data = str_data[:]
str_data = str_data.replace('{}', "")
str_data = str_data.replace('}{', "}///{")
str_datas = str_data.split('///')
str_datas = [x.replace("'", '"') for x in str_datas]
num = 0


for str_data in str_datas:
    num += 1

    try:
        dict_data = literal_eval(str_data)
        json_data = json.loads(str_data)
        result.append(dict_data)
    except:
        print("Fail", num)


# str_data = str_data.replace('},{', '}///{')

# str_data = str_data.replace("'", '"')
# str_data = '[' + str_data[0:-1] + ']'

# str_datas = str_data.split("///")
# print(len(str_datas))
# str_data = '[' + str_data[1:-1] + ',]'
# str_data = '[' + str_data[1:] + ']'
# idx = 407516
# print(str_data[idx-20:idx+20])
# print(str_data[:10])
# print(str_data[-1])
# f = open("../test_result.txt", "w", encoding='utf-8')
# f.write(str_data)
# f.close()

# json_data = json.loads(str_data, encoding='utf-8')
print(len(result))
with open('C:/Users/jlee/Crawling-Car-Info/Crawling/from_server/result21_t.json', 'w', encoding='utf-8-sig') as ff:
    json.dump(result, ff, indent=4, ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result1.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[:10000], ff, indent=4, ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result2.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[10000:20000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result3.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[20000:30000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result4.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[30000:40000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result5.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[40000:50000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result6.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[50000:60000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result7.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[60000:70000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result8.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[70000:80000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result9.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[80000:90000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result10.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[90000:100000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result11.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[100000:110000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result12.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[110000:120000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result13.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[120000:130000], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
# with open('C:/Users/jlee/Desktop/result14.json'.format(num=num), 'w', encoding='utf-8-sig') as ff:
#     json.dump(result[130000:], ff, indent=4,
#               ensure_ascii=False, sort_keys=True)
