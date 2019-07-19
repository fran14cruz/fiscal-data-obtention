import json
import requests


def get_data(FN, FD, FPD):
    '''Выводит данные чека по данным
        из QR-кода.

        Если чек в ОФД не найден, то выводится None

        Первый аргумент - фискальный номер,
        Второй аргумент - фискальный документ,
        Третий аргумент - фискальный признак
        '''

    session = requests.Session()

    data = json.dumps({"fiscalDriveId": str(FN), "fiscalDocumentNumber": str(FD), "fiscalId": str(FPD)})
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru,en;q=0.9,ru-RU;q=0.8,en-US;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "88",
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": "_ga=GA1.2.897925840.1563277337; _gid=GA1.2.1030907507.1563277337; PLAY_LANG=ru; XSRF-TOKEN=5ea8f6e97cb2c904efcf50c62e767cad8d64f8de-1563277343217-66e2d8c3784527ee6b83aacc; _ym_uid=1563277337608491586; _ym_d=1563277337; _ym_isad=1; X-ANONYMOUS=3u3rwr9bubbnkyg6nh5qyog98; flocktory-uuid=eb32ddb6-1c97-458f-a968-7041b13313d2-1",
        "Host": "consumer.1-ofd.ru",
        "Origin": "https://consumer.1-ofd.ru",
        "Referer": "https://consumer.1-ofd.ru/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "X-XSRF-TOKEN": "5ea8f6e97cb2c904efcf50c62e767cad8d64f8de-1563277343217-66e2d8c3784527ee6b83aacc"
    }

    try:
        r = session.post('https://consumer.1-ofd.ru/api/tickets/find-ticket', data=data, headers=headers)
    except:
        print("Не удалось установить содинение")
        return None
    data = json.loads(r.text)
    if data['status'] == 1:
        check = str(r.text[r.text.find(":") + 2:r.text.find(",") - 1])
        url = "https://consumer.1-ofd.ru/api/tickets/ticket/" + check
        response = requests.get(url)
        data = json.loads(response.text)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        save = {}
        save["cash_total_sum"] = int(data["ticket"]["options"]["cashTotalSum"])
        save["date_time"] = (data["ticket"]["options"]["dateTime"])
        save["ecash_total_sum"] = int(data["ticket"]["options"]["ecashTotalSum"])
        save["fiscal_doc_num"] = FD
        save["fiscal_drive_num"] = str(FN)
        save["fiscal_sign"] = FPD
        save["inn"] = str(data["kkmExtraInfo"]["owner"]["inn"])
        save["kkt_reg_id"] = str(data["ticket"]["options"]["kktRegId"])
        if "nds10" in data["ticket"]["options"]:
            save["nds10"] = int(data["ticket"]["options"]["nds10"])
        else:
            save["nds10"] = None
        if "nds18" in data["ticket"]["options"]:
            save["nds18"] = int(data["ticket"]["options"]["nds18"])
        else:
            save["nds18"] = None
        save["operationType"] = int(data["ticket"]["options"]["operationType"])
        save["operator"] = str(data["ticket"]["options"]["operator"])
        save["org_name"] = str(data["orgTitle"])
        save["receipt_code"] = 3
        save["req_num"] = int(data["ticket"]["options"]["requestNumber"])
        save["shift_num"] = int(data["ticket"]["options"]["shiftNumber"])
        save["tax_type"] = int(data["ticket"]["options"]["taxationType"])
        save["total_sum"] = int(data["ticket"]["options"]["totalSum"])
        save["retail_place_address"] = str(data["retailPlaceAddress"])

        save["items"] = []
        j = 0
        if "items" in data["ticket"]:
            for i in data["ticket"]["items"]:
                save["items"].append({"name": str(i["options"]["name"]), "price": int(i["price"]),
                                      "quantity": int(i["quantity"]), "sum": int(i["sum"]), "nds10": None,
                                      "nds18": None})
                if 'nds10' in i["options"]:
                    save["items"][j]['nds10'] = int(i["options"]['nds10'])
                if 'nds18' in i["options"]:
                    save["items"][j]['nds18'] = int(i["options"]['nds18'])
                j += 1

        print("Чек найден")
        return save
    else:
        print("Чек не найден")
