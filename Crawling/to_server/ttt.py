from ast import literal_eval
import json
import os


def process_json():

    result = list()
    for num in range(1, 50):
        print(num)
        with open('C:/Users/jlee/Desktop/AWS/result{num}_t.json'.format(num=num), encoding='utf-8-sig', errors='ignore') as f:
            str_data = f.read()
        str_data = str(str_data)
        str_data = str_data[:]
        str_data = str_data.replace('{}', "")
        str_data = str_data.replace('}{', "}///{")
        str_datas = str_data.split('///')
        str_datas = [x.replace("'", '"') for x in str_datas]
        num_s = 0
        str_datas = list(set(str_datas))
        for str_data in str_datas:
            num_s += 1
            try:
                dict_data = literal_eval(str_data)
                json_data = json.loads(str_data)
                if dict_data['noRegisterPeriod'] == 'none':
                    dict_data['noRegisterPeriod'] = 'null'
                result.append(dict_data)
            except:
                print("Fail", num_s)

    print("총 json에 차량 개수 ", len(result))

    with open('C:/Users/jlee/Desktop/AWS/result.json', 'w', encoding='utf-8-sig') as ff:
        json.dump(result, ff, indent=4, ensure_ascii=False, sort_keys=True)


###main ##
process_json()

# for num in range(32, 49):
#     result = list()
#     with open('C:/Users/jlee/Desktop/result{num}_t.json'.format(num=num), encoding='utf-8-sig', errors='ignore') as f:
#         str_data = f.read()
#     str_data = str_data.replace('{}', "")
#     str_data = str_data.replace('}{', "}///{")
#     str_datas = str_data.split('///')

#     for num, str_data in enumerate(str_datas):
#         if num == 499:
#             break
#         dict_data = literal_eval(str_data)
#         with open('C:/Users/jlee/Desktop/result50_t.json', 'a', encoding='utf-8-sig') as ff:
#             json.dump(dict_data, ff, indent=4,
#                       ensure_ascii=False, sort_keys=True)
