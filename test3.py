


# import pymysql
# import requests
# import json
# import time
# import re
#
# ''' 创建货件'''
#
# def mysql_xiugai(fk,id):
#     conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',charset='utf8')
#     cursor = conn.cursor()
#     sql = r'update tp set fk=%s where id = %s'
#     try:
#         ret = cursor.execute(sql, [fk, id])
#         conn.commit()
#         return ret
#     except Exception as e:
#         print(e)
#         return 0
#     finally:
#         cursor.close()
#         conn.close()
#
# def mysql_cx():
#     conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',charset='utf8')
#     sql = r'select id,sku,suocang,guojia,sjbh,iid,addr from tp where fk=1'
#     cursor = conn.cursor()
#     try:
#         cursor.execute(sql)
#         ret = cursor.fetchall()
#         return ret
#     except Exception as e:
#         print(e)
#         return 0
#     finally:
#         cursor.close()
#         conn.close()
#
#
# def fsqq():
#     ret = mysql_cx()
#     if ret:
#         #print(ret,22)
#         suocang = ''
#         addr = ''
#         if ret[0][2] == '0' or ret[0][2] == 0:
#             suocang = ''
#         else:
#             suocang = ret[0][2]
#
#
#         if ret[0][6] == '0' or ret[0][6] == 0:
#             addr = ''
#         else:
#             addr = ret[0][6]
#         # 定义正则表达式
#         pattern = r"(B[A-Z0-9][^￥]+)￥([^￥]+)￥([^￥][^,|^，]?)"
#
#         # 使用re模块的findall()函数进行匹配
#         matches = re.findall(pattern, ret[0][1])
#
#         # 打印匹配结果
#         print(matches)
#         asinsku = ''
#         for matche in matches:
#             sss = matche[1] + '￥' + matche[2]
#             if asinsku:
#                 asinsku = asinsku + ',' + sss
#             else:
#                 asinsku = sss
#         print(asinsku)
#         data1 = {
#             "Id": str(ret[0][0]),
#             "货件sku": asinsku,
#             "目标": suocang,
#             "国家": ret[0][3],
#             "店铺": ret[0][4],
#             "令牌": ret[0][5],
#             "地址": addr,
#             "跟卖sku": ""
#         }
#         data = json.dumps(data1, ensure_ascii=False).encode('utf-8')
#
#         print(data1)
#         headers = {
#             'Content-Type':'application/json',
#             'user-agent':'PostmanRuntime/7.30.0Accept: */*',
#             'Postman-Token':'c50aedda-5ad8-4dcb-ac82-ad68ec8f0609',
#             'Host': '43.153.11.159:50001',
#             'Accept-Encoding': 'gzip, deflate, br'
#         }
#         response = requests.post(url='http://43.153.11.159:50001/Working_SCTP', data=data, headers=headers)
#         if response.status_code == 200:
#             print('创建货件反馈：{0}'.format(response))
#             ret1 = mysql_xiugai(response.text, ret[0][0])
#             if ret1:
#                 return '写入数据库成功:{0}---{1}'.format(ret1, response.text)
#             else:
#                 return '数据库发送失败：{0}'.format(ret1)
#         else:
#             return '请求发送失败：{0}'.format(response.status_code)
#     else:
#         return 0
#
#
#
#
# if __name__ == '__main__':
#     '''发送突破请求'''
#     while True:
#         try:
#             ret = fsqq()
#             if ret:
#                 print(ret, 11)
#                 time.sleep(5)
#             else:
#                 print('突破没找到需要发送的数据！')
#                 time.sleep(30)
#         except Exception as e:
#             print(e)
#             time.sleep(10)
#             continue

#A3HX9RXGD89CB5
#美西
#amzn.mws.32c28324-8127-61fb-ed83-a8e7520c1733
#FJ-DZM7-30XS
#US


import logging
import pymysql
import requests
import json
import time
import re

# 配置日志记录器
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='test3.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 将控制台处理器添加到日志器中
logging.getLogger('').addHandler(console)

# 记录日志信息
#logging.info('This is an info message')
#logging.error('This is an error message')

DB_HOST = '43.142.154.185'
DB_PORT = 3306
DB_USER = 'test01'
DB_PASSWORD = 'zzzfsg3574.'
DB_NAME = 'amazon'

API_URL = 'http://43.153.11.159:50001/Working_SCTP'


def update_fk_in_db(fk, id):
    sql = 'UPDATE tp SET fk=%s WHERE id=%s'
    try:
        with pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
                             charset='utf8') as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, [fk, id])
                conn.commit()
                return cursor.rowcount
    except Exception as e:
        logging.error(f'Error in update_fk_in_db: {e}')
        return 0


def get_pending_shipments_from_db():
    sql = 'SELECT id, sku, suocang, guojia, sjbh, iid, addr, username FROM tp WHERE fk=1'
    try:
        with pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME,
                             charset='utf8') as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
    except Exception as e:
        logging.error(f'Error in get_pending_shipments_from_db: {e}')
        return []


def create_shipment():
    pending_shipments = get_pending_shipments_from_db()
    if not pending_shipments:
        return 0

    id, sku, suocang, guojia, sjbh, iid, addr, username = pending_shipments[0]
    logging.info(f'{username}：开始执行建仓...')
    asinsku = ''
    pattern = r"(B[A-Z0-9][^￥]+)￥([^￥]+)￥([^￥][^,|^，]?)"
    matches = re.findall(pattern, sku)
    for match in matches:
        sss = f"{match[1]}￥{match[2]}"
        if asinsku:
            asinsku += f",{sss}"
        else:
            asinsku = sss

    data = {
        "Id": str(id),
        "货件sku": asinsku,
        "目标": suocang if suocang != '0' else '',
        "国家": guojia,
        "店铺": sjbh,
        "令牌": iid if iid != '0' else '',
        "地址": addr if addr != '0' else '',
        "跟卖sku": ""
    }
    logging.info(f'{username}：建仓数据为：{data}')
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'PostmanRuntime/7.30.0Accept: */*',
        'Postman-Token': 'c50aedda-5ad8-4dcb-ac82-ad68ec8f0609',
        'Host': '43.153.11.159:50001',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    try:
        response = requests.post(url=API_URL, data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                                 headers=headers)
        response.raise_for_status()
        ret = update_fk_in_db(response.text, id)
        if ret:
            return f'写入数据库成功:{ret}---{response.text}'
        else:
            return f'数据库发送失败：{ret}'

    except requests.exceptions.RequestException as e:
        logging.error(f'Error in create_shipment: {e}')
        return f'请求发送失败：{e}'

if __name__ == '__main__':
    '''发送突破请求'''
    while True:
        try:
            ret = create_shipment()
            if ret:
                logging.info(f'执行结果：{ret}')
                time.sleep(5)
            else:
                logging.info('建仓没找到需要发送的数据！')
                time.sleep(30)
        except Exception as e:
            logging.error(f'Error in main: {e}')
            time.sleep(10)
            continue