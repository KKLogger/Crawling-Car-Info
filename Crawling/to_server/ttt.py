import json

with open('C:/Users/jlee/Desktop/KB차차차 크롤링/result_all.json', encoding='utf-8-sig') as f:
    json_datas = json.load(f)
for json_data in json_datas:
    if json_data['CHECK_INNER'] == "null" and json_data['CHECK_OUTER'] == "null":
        json_data['RegistrationID'] = "null"
        json_data['MotorType'] = 'null'
        json_data['WarrantyType'] = 'null'
        json_data['IssueDt'] = 'null'
with open('C:/Users/jlee/Desktop/KB차차차 크롤링/result_all_t.json', 'w', encoding='utf-8-sig') as ff:
    json.dump(json_datas, ff, indent=4, ensure_ascii=False, sort_keys=True)
