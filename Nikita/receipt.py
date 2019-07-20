import json
import psycopg2 as psql


def get(FN, FD, FPD):
    conn = psql.connect(dbname='check', user='postgres', password='postgres', host='localhost')
    cur = conn.cursor()
    data = {}

    FN = str(FN)
    FD = str(FD)
    FPD = str(FPD)

    cur.execute('''SELECT cash_total_sum, date_time, ecash_total_sum, fiscal_doc_num, 
     fiscal_drive_num, fiscal_sign, inn, kkt_reg_id, nds10, nds18, operation_type,
     operator, org_name, receipt_code, req_num, shift_num, tax_type, total_sum, retail_place_address, id 
     FROM receipts WHERE fiscal_drive_num = %s and fiscal_doc_num = %s and fiscal_sign = %s''',
                                             (FN, FD, FPD))
    conn.commit()
    for row in cur:
        data['cash_total_sum'] = row[0]
        data['date_time'] = row[1]
        data['ecash_total_sum'] = row[2]
        data['fiscal_doc_num'] = row[3]
        data['fiscal_drive_num'] = row[4]
        data['fiscal_sign'] = row[5]
        data['inn'] = row[6]
        data['kkt_reg_id'] = row[7]
        data['nds10'] = row[8]
        data['nds18'] = row[9]
        data['operationType'] = row[10]
        data['operator'] = row[11]
        data['org_name'] = row[12]
        data['receipt_code'] = row[13]
        data['req_num'] = row[14]
        data['shift_num'] = row[15]
        data['tax_type'] = row[16]
        data['total_sum'] = row[17]
        data['retail_place_address'] = row[18]

        items_id = row[19]
    data["items"] = []

    cur.execute('''SELECT name, price, quantity, sum, nds10, nds18 FROM purchases WHERE receipt = %s''',
                (items_id,))
    conn.commit()
    for row in cur:
        data["items"].append({"name": row[0], "price": row[1], "quantity": row[2], "sum": row[3],
                              "nds10": row[4], "nds18": row[5]})

    conn.close()
    cur.close()

    return data
    #if data:
    #    return data
    #else:
        #print('Ошибка. Чек не был получен из БД')
        #return None




def save(data):

    data_exists = get(data["fiscal_drive_num"], data["fiscal_doc_num"], data["fiscal_sign"])
    if data_exists:
        print('Чек уже существует в БД')
    else:
        conn = psql.connect(dbname='check', user='postgres', password='postgres', host='localhost')
        cur = conn.cursor()

        cur.execute('''INSERT INTO receipts (cash_total_sum, date_time, ecash_total_sum, fiscal_doc_num, 
             fiscal_drive_num, fiscal_sign, inn, kkt_reg_id, nds10, nds18, operation_type,
             operator, org_name, receipt_code, req_num, shift_num, tax_type, total_sum, retail_place_address) 
             VALUES (%s, to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            (data["cash_total_sum"], data["date_time"], data["ecash_total_sum"], data["fiscal_doc_num"],
            data["fiscal_drive_num"], data["fiscal_sign"], data["inn"], data["kkt_reg_id"], data["nds10"],
            data["nds18"], data["operationType"], data["operator"], data["org_name"], data["receipt_code"],
            data["req_num"], data["shift_num"], data["tax_type"], data["total_sum"], data["retail_place_address"]))
        conn.commit()
        if cur.rowcount:
            print('Успешная запись в таблицу receipts')
        else:
            print('Ошибка. Не удалось сделать запись в таблицу receipts')

        cur.execute('''SELECT id FROM receipts 
                    WHERE fiscal_drive_num = %s and fiscal_doc_num = %s and fiscal_sign = %s''',
                    (data["fiscal_drive_num"], data["fiscal_doc_num"], data["fiscal_sign"]))
        conn.commit()

        receipt_id = ''
        for row in cur:
            receipt_id = row[0]
        for item in data["items"]:
            cur.execute('''INSERT INTO purchases (name, price, quantity, sum, nds10, nds18, receipt) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                        (item["name"], item["price"], item["quantity"], item["sum"],
                         item["nds10"], item["nds18"], receipt_id))
            conn.commit()
            if cur.rowcount:
                print('Успешная запись в таблицу purchases')
            else:
                print('Ошибка. Не удалось сделать запись в таблицу purchases')

        conn.close()
        cur.close()


