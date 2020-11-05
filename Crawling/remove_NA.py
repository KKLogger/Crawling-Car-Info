import multiprocessing
import json
import pandas as pd

# df = pd.read_json('',
#                   encoding='utf-8-sig')
# print(df)
with open('C:/Users/jlee/Desktop/result.json', encoding='utf-8', errors='ignore') as f:
    str_data = f.read()
str_data = str(str_data)
str_data = str_data.replace('}{', "},{")

# str_data = str_data.replace('},{', '}///{')

# str_data = str_data.replace("'", '"')
# str_data = '[' + str_data[0:-1] + ']'

# str_datas = str_data.split("///")
# print(len(str_datas))
# str_data = '[' + str_data[1:-1] + ',]'
str_data = '[' + str_data[1:] + ']'
idx = 407516
print(str_data[idx-20:idx+20])
# print(str_data[:10])
# print(str_data[-1])
# f = open("../test_result.txt", "w", encoding='utf-8')
# f.write(str_data)
# f.close()

json_data = json.loads(str_data, encoding='utf-8')

with open('C:/Users/jlee/Desktop/result1.json', 'w', encoding='utf-8') as ff:
    json.dump(json_data, ff, indent=4, ensure_ascii=True, sort_keys=True)
