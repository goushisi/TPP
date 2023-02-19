#
# import pymysql
# import requests
# import json
# import time
#
# '''多渠道'''
#
#
# def mysql_xiugai(dqdfk, id):
#     conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',charset='utf8')
#     cursor = conn.cursor()
#     sql = r'update tp set dqdfk=%s where id = %s'
#     try:
#         ret = cursor.execute(sql, [dqdfk, id])
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
#     sql = r'select id,sku,suocang,guojia,sjbh,iid,dqd from tp where dqd != "0" and sjbh != "0" and iid != "0" and zt = 1 and dqdfk = 1'
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
# def duoqudao():
#     ret = mysql_cx()
#     if ret:
#         suocang = ''
#         if ret[0][2] == '0':
#             suocang = ''
#         data = json.dumps({
#             "Id": str(ret[0][0]),
#             "货件sku": "",
#             "目标": suocang,
#             "国家": ret[0][3],
#             "店铺": ret[0][4],
#             "令牌": ret[0][5],
#             "多渠道": ret[0][6],
#             "跟卖sku": ""
#         }, ensure_ascii=False).encode('utf-8')
#         print(data)
#         headers = {
#             'Content-Type': 'application/json',
#             'user-agent': 'PostmanRuntime/7.30.0Accept: */*',
#             'Postman-Token': 'c50aedda-5ad8-4dcb-ac82-ad68ec8f0609',
#             'Host': '43.153.11.159:50001',
#             'Accept-Encoding': 'gzip, deflate, br'
#         }
#         response = requests.post(url='http://43.153.11.159:50001/Working_SCTP', data=data, headers=headers)
#         if response.status_code == 200:
#             print('锁仓反馈：{0}'.format(response))
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
# if __name__ == '__main__':
#     '''发送突破请求'''
#     while True:
#         try:
#             ret = duoqudao()
#             if ret:
#                 print(ret)
#                 time.sleep(5)
#             else:
#                 print('多渠道没找到需要发送的数据！')
#                 time.sleep(30)
#         except Exception as e:
#             print(e)
#             time.sleep(10)
#             continue








import requests
import json
import time
import logging
import pymysql

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

def connect_db():
    return pymysql.connect(
        host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon', charset='utf8'
    )


def update_database(dqdfk, id):
    with connect_db() as conn, conn.cursor() as cursor:
        sql = r'update tp set dqdfk=%s where id = %s'
        try:
            ret = cursor.execute(sql, [dqdfk, id])
            conn.commit()
            return ret
        except Exception as e:
            logging.error(e)
            return 0


def get_data_from_database():
    with connect_db() as conn, conn.cursor() as cursor:
        sql = r'select id,sku,suocang,guojia,sjbh,iid,dqd,username from tp where dqd != "0" and sjbh != "0" and iid != "0" and zt = 1 and dqdfk = 1'
        try:
            cursor.execute(sql)
            ret = cursor.fetchall()
            return ret
        except Exception as e:
            logging.error(e)
            return 0


def send_duoqudao_request():
    data_from_database = get_data_from_database()
    if not data_from_database:
        return 0
    id, sku, suocang, guojia, sjbh, iid, dqd, username = data_from_database[0]
    logging.info(f'{username}：开始执行多渠道...')
    suocang = '' if not suocang else suocang
    data = {
        "id": str(id),
        "货件sku": "",
        "目标": suocang,
        "国家": guojia,
        "店铺": sjbh,
        "令牌": iid,
        "多渠道": dqd,
        "跟卖sku": ""
    }
    logging.info(f'{username}：多渠道数据为：{data}')
    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'PostmanRuntime/7.30.0Accept: */*',
        'Postman-Token': 'c50aedda-5ad8-4dcb-ac82-ad68ec8f0609',
        'Host': '43.153.11.159:50001',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    try:
        with requests.post('http://43.153.11.159:50001/Working_SCTP', data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers=headers, timeout=5) as response:
            response.raise_for_status()
            message = '锁仓反馈：{0}'.format(response)
            logging.info(message)
            ret = update_database(response.text, id)
            if ret:
                message = '写入数据库成功:{0}---{1}'.format(ret, response.text)
                logging.info(message)
                return message
            else:
                message = '数据库发送失败：{0}'.format(ret)
                logging.error(message)
                return message
    except requests.exceptions.RequestException as e:
        message = '请求发送失败：{0}'.format(e)
        logging.error(message)
        return message

if __name__ == '__main__':
    while True:
        try:
            ret = send_duoqudao_request()
            if ret:
                logging.info(ret)
                time.sleep(5)
            else:
                logging.info('多渠道没找到需要发送的数据！')
                time.sleep(30)
        except Exception as e:
            logging.exception('程序运行出现异常：{0}'.format(e))
            time.sleep(10)
            continue