import multiprocessing
import json
import pandas as pd
from ast import literal_eval


result = list()
with open('C:/Users/jlee/Desktop/result.json', encoding='utf-8-sig', errors='ignore') as f:
    str_data = f.read()
str_data = str(str_data)
str_data = str_data[1:]
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
        print(str_data)
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
with open('C:/Users/jlee/Desktop/result1.json', 'w', encoding='utf-8-sig') as ff:
    json.dump(result, ff, indent=4, ensure_ascii=False, sort_keys=True)
