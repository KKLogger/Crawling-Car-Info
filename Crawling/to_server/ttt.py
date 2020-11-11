from ast import literal_eval
import json
import os


def process_json():

    result = list()
    for num in range(1, 51):
        with open('C:/Users/jlee/Desktop/result{num}_t.json'.format(num=num), encoding='utf-8-sig', errors='ignore') as f:
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
                if dict_data['noRegisterPeriod'] == 'none':
                    dict_data['noRegisterPeriod'] = 'null'
                result.append(dict_data)
            except:
                print("Fail", num)

    print("총 json에 차량 개수 ", len(result))

    with open('result.json', 'w', encoding='utf-8-sig') as ff:
        json.dump(result, ff, indent=4, ensure_ascii=False, sort_keys=True)


###main ##
process_json()
