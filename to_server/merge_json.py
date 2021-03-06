import json
from ast import literal_eval
import os
from datetime import datetime
import sys

"""
>>> 수집한 json 병합하는 코드
"""
# local_path = "/home/centos/result_from_servers/"
# day = datetime.today().strftime("%Y%m%d")
day = 20201231
date = day % 10000
local_path = f"D:/desktop/아름드리/{date}/"

if __name__ == "__main__":
    result = list()
    str_list = list()
    data_num =0
    for server_num in range(1, 31):
        try:
            with open(
                local_path
                + "{day}.result{server_num}_t.json".format(server_num=server_num, day=day),
                encoding="utf-8-sig",
                errors="ignore",
            ) as f:
                str_data = f.read()
            data_num +=1
            str_data = str(str_data)
            str_data = str_data[:]
            str_data = str_data.replace("{}", "")
            str_data = str_data.replace("}{", "}///{")
            str_datas = str_data.split("///")
            str_datas = [x.replace("'", '"') for x in str_datas]
            str_list = str_list + str_datas
            print(server_num)
            str_list = list(set(str_list))
        except:
            continue
        num = 0
    for str_data in str_list:
        num += 1
        try:
            dict_data = literal_eval(str_data)
            json_data = json.loads(str_data)
            result.append(dict_data)
        except:
            print("Fail", num)

    print("총 json에 차량 개수 ", len(result))
    print('json 파일의 개수 ',data_num)
    with open(
        local_path + "KB차차차,{num}건,{day}.json".format(num=len(result), day=day),
        "w",
        encoding="utf-8-sig",
    ) as ff:
        json.dump(result, ff, indent=4, ensure_ascii=False, sort_keys=True)
