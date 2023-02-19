from gevent import monkey
from flask import g, request, Flask, current_app, jsonify, json
import jwt
from jwt import exceptions
import functools
import datetime
import random
import pymysql
import time
from flask_cors import CORS
import Debug
from gevent import pywsgi
#from dotenv import load_dotenv

monkey.patch_all()
app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)
# 处理中文编码
app.config['JSON_AS_ASCII'] = False
#load_dotenv(dotenv_path='.flaskenv', override=True)

# 跨域支持
# def after_request(resp):
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp
#
#
# app.after_request(after_request)

# 构造header
headers = {
    'typ': 'jwt',
    'alg': 'HS256'
}

# 密钥
SALT = 'iv%i6xo7l8_t9bf_u!8#g#m*)*+ej@bek6)(@u3kh*42+unjv='




def create_token(username, password):
    '''构造payload'''
    payload = {
        'username': username,
        'password': password,  # 自定义用户ID
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # 超时时间
    }
    result = jwt.encode(payload=payload, key=SALT, algorithm="HS256", headers=headers)
    #logger.info('加码', result)
    return result

def verify_jwt():
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
        token = auth[7:]
        #logger.info('解码1', token)


    # if not secret:
    #     secret = current_app.config['JWT_SECRET']

    try:
        payload = jwt.decode(token, SALT, algorithms=['HS256'])
        return payload
    except exceptions.ExpiredSignatureError:  # 'token已失效'
        return 1
    except jwt.DecodeError:  # 'token认证失败'
        return 2
    except jwt.InvalidTokenError:  # '非法的token'
        return 3

def login_required(f):
    '让装饰器装饰的函数属性不会变 -- name属性'
    '第1种方法,使用functools模块的wraps装饰内部函数'

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            #logger.info(g.username,1313)
            if g.username == 1:
                return {'code': 4001, 'message': 'token已失效'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': 'token认证失败'}, 401
            elif g.username == 2:
                return {'code': 4001, 'message': '非法的token'}, 401
            else:
                return f(*args, **kwargs)
        except BaseException as e:
            return {'code': 4001, 'message': '请先登录认证.'}, 401

    '第2种方法,在返回内部函数之前,先修改wrapper的name属性'
    # wrapper.__name__ = f.__name__
    return wrapper

@app.before_request
def jwt_authentication():
    """
    1.获取请求头Authorization中的token
    2.判断是否以 Bearer开头
    3.使用jwt模块进行校验
    4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存
    """

    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        "提取token 0-6 被Bearer和空格占用 取下标7以后的所有字符"
        token = auth[7:]
        #logger.info('解码', token)
        "校验token"
        g.username = None
        try:
            "判断token的校验结果"
            payload = jwt.decode(token, SALT, algorithms=['HS256'])
            "获取载荷中的信息赋值给g对象"
            g.username = payload.get('username')
            print(payload.get('username'), 12123)
        except exceptions.ExpiredSignatureError:  # 'token已失效'
            g.username = 1
        except jwt.DecodeError:  # 'token认证失败'
            g.username = 2
        except jwt.InvalidTokenError:  # '非法的token'
            g.username = 3
        #logger.info(g.username,2211)



def mysql_login(password):
    '''登陆验证'''
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test02', passwd='addshlt', db='amazon',
                           charset='utf8')
    cursor = conn.cursor()
    sql = r'select id,username,password from user_login where password = %s and type = "TP"'
    cursor.execute(sql, [password])
    ret = cursor.fetchone()
    cursor.close()
    conn.close()
    return ret

def mysql_selnoe(sjId):
    ''' 根据突破编号查询信息'''
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',
                           charset='utf8')
    sql = r'select guojia,cookie,sjbh,iid,username,fk from tp where sjId = %s'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, [sjId])
        ret = cursor.fetchone()
        return ret
    except Exception as e:
        logger.info(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_all(username, sjId):
    '''查询给用户显示的数据'''
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test02', passwd='addshlt', db='amazon',
                           charset='utf8')
    cursor = conn.cursor()
    if sjId != '':
        sql = r'select * from tp where username = %s and sjId = %s'
        cursor.execute(sql, [username, sjId])
    else:
        sql = r'select * from tp where username = %s order by id desc'
        cursor.execute(sql, [username])
    try:
        ret = cursor.fetchall()
        return ret
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_xiugaifk(sjId):
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon', charset='utf8')
    cursor = conn.cursor()
    print(sjId)
    sql = r'update tp set fk = 1,count = count + 1 where sjId = %s'
    try:
        ret = cursor.execute(sql, [sjId])
        conn.commit()
        print(ret)
        return ret
    except Exception as e:
        logger.info(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_charushuju(cookie, guojia, suocang, sku, sjId, dqd, username, addr):
    '''创建一条任务'''
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',
                           charset='utf8')
    cursor = conn.cursor()
    sql = r'insert into tp VALUES (0,%s,%s,%s,%s,%s,0,"0","0",0,%s,1,%s,%s,%s,0)'

    try:
        ret = cursor.execute(sql, [sjId, sku, suocang, guojia, cookie, dqd, username, addr, dt_string])
        conn.commit()

        return ret
    except Exception as e:
        logger.info(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_cx(sjId):
    ''' 根据突破编号，查询任务反馈（feedback）以及多渠道反馈（feedback）'''
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon', charset='utf8')
    sql = r'select fk,dqdfk from tp where sjId = %s'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, [sjId])
        ret = cursor.fetchone()
        return ret
    except Exception as e:
        logger.info(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_xiugaisku(sjId, sku, addr, suocang):
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',
                           charset='utf8')
    cursor = conn.cursor()
    if sku == '' and addr == '' and suocang == '':
        logger.info('修改的3个只为空，反馈失败')
        return 0
    try:
        sql = ''
        ret = ''
        if sku != '' and addr != '' and suocang != '':
            #两个都不等于0
            logger.info('三个值都不为空！，允许操作')
            sql = r'update tp set sku = %s,addr = %s,suocang = %s where sjId = %s'
            ret = cursor.execute(sql, [sku, addr, sjId, suocang])
        elif sku != '' and addr == '' and suocang == '':
            #sku不为0，addr为0
            logger.info('SKU不为空')
            sql = r'update tp set sku = %s where sjId = %s'
            ret = cursor.execute(sql, [sku, sjId])
        elif sku == '' and addr != '' and suocang == '':
            #sku为0，addr不为0
            logger.info('地址不为空')
            sql = r'update tp set addr = %s where sjId = %s'
            ret = cursor.execute(sql, [addr, sjId])
        elif sku == '' and addr == '' and suocang != '':
            logger.info('锁仓不为空')
            sql = r'update tp set suocang = %s where sjId = %s'
            ret = cursor.execute(sql, [suocang, sjId])
        elif sku != '' and addr != '' and suocang == '':
            logger.info('SKU不为空，地址不为空')
            sql = r'update tp set sku = %s,addr = %s where sjId = %s'
            ret = cursor.execute(sql, [sku, addr, sjId])
        elif sku == '' and addr != '' and suocang != '':
            logger.info('地址不为空，锁仓不为空')
            sql = r'update tp set addr = %s,suocang = %s where sjId = %s'
            ret = cursor.execute(sql, [addr, suocang, sjId])
        elif sku != '' and addr == '' and suocang != '':
            logger.info('SKU不为空，锁仓不为空')
            sql = r'update tp set sku = %s,suocang = %s where sjId = %s'
            ret = cursor.execute(sql, [sku, suocang, sjId])
        else:
            logger.info('{0}，信息填写错误')
            return 0
        conn.commit()
        return ret
    except Exception as e:
        logger.info(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_zengjiahuojian(rsjId, sku, suocang, guojia, cookie, sjbh, iid, dqd, username, addr):
    '''新增一条'''
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',
                           charset='utf8')
    cursor = conn.cursor()
    try:

        sql = ''
        if dqd == '0':
            logger.info('{0}：没有多渠道信息'.format(rsjId))
            sql = r'insert into tp VALUES (0,%s,%s,%s,%s,%s,1,%s,%s,1,%s,1,%s,%s,%s,0)'
            ret = cursor.execute(sql, [rsjId, sku, suocang, guojia, cookie, sjbh, iid, dqd, username, addr, dt_string])
        else:
            logger.info('{0}：有多渠道信息'.format(rsjId))
            sql = r'insert into tp VALUES (0,%s,%s,%s,%s,%s,1,%s,%s,0,%s,1,%s,%s,%s,0)'
            ret = cursor.execute(sql, [rsjId, sku, suocang, guojia, cookie, sjbh, iid, dqd, username, addr, dt_string])
        conn.commit()
        return ret
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        conn.close()



@app.route('/login', methods=['post'])
def login_verification():
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    '''登录功能'''
    password = request.values.get('user_id')
    ret = mysql_login(password)

    if ret:
        logger.info(ret)
        logger.info('{0}，{1},以成功登录！'.format(dt_string, ret[1]))
        tokens = create_token(ret[1], password)
        #request.headers.set('Authorization', tokens)
        return tokens
    else:
        logger.info('登录失败！')
        return 'null'

@app.route('/gogo', methods=['post'])
@login_required
def gogo():
    '''参数接收'''
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    cookie = request.values.get('cookie')
    guojia = request.values.get('guojia')
    suocang = request.values.get('suocang')
    sku = request.values.get('sku')
    dqd = request.values.get('dqd')
    sjId = str(random.randint(100, 1000))+'-'+str(time.time())
    addr = request.values.get('addr')

    logger.info('{0}---{1}：---------------------提交参数---------------------'.format(dt_string, g.username))
    logger.info('{0}---{1}：cookiek：{2}'.format(dt_string, g.username, cookie[0:10]))
    logger.info('{0}---{1}：国家：{2}'.format(dt_string, g.username, guojia))
    logger.info('{0}---{1}：锁仓：{2}'.format(dt_string, g.username, suocang))
    logger.info('{0}---{1}：SKU：{2}'.format(dt_string, g.username, sku))
    logger.info('{0}---{1}：多渠道信息：{2}'.format(dt_string, g.username, dqd))
    logger.info('{0}---{1}：任务编号：{2}'.format(dt_string, g.username, sjId,))
    logger.info('{0}---{1}：发货地址：{2}'.format(dt_string, g.username, addr))
    logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
    if cookie == '' or guojia == '' or suocang == '' or sku == '' or sjId == '' or dqd == '' or addr == '':
        return 0
    print(1122)
    ret = mysql_charushuju(cookie, guojia, suocang, sku, sjId, dqd, g.username, addr)
    print(ret)
    if ret:
        logger.info('{0}---{1}：,---------------------提交结果---------------------'.format(dt_string, g.username))
        logger.info('{0}---{1}：结果{2}'.format(dt_string, g.username, ret))
        logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
        return sjId

@app.route('/out', methods=['get','post'])
@login_required
def out():
    #user = verify_jwt()
    #logger.info(user)
    #logger.info(user['username'])
    logger.info(g.username)
    return json.dumps(g.username, ensure_ascii=False)

@app.route('/showuserdata', methods=['post'])
@login_required
def showuserdata():
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    sjId1 = request.values.get('sjId1')
    logger.info('{0},显示数据：{1}'.format(dt_string, sjId1))
    username = g.username #获取用户名
    datas = mysql_all(username, sjId1)
    if datas:
        logger.info('{0}---{1}：显示成功'.format(dt_string, g.username))
        return json.dumps(datas, ensure_ascii=False)
    else:
        logger.info('{0}---{1}：显示失败'.format(dt_string, g.username))
        return json.dumps('失败', ensure_ascii=False)

@app.route('/jiancang', methods=['post'])
@login_required
def jiancang():
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    sjId = request.values.get('sjId')
    logger.info('{0}---{1}：---------------------提交任务编号---------------------'.format(dt_string, g.username))
    logger.info('{0}---{1}：任务编号：{2}'.format(dt_string, g.username, sjId))
    logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
    if sjId == '':
        return 'null'
    selnoe = mysql_selnoe(sjId)
    sjbh = selnoe[2]
    iid = selnoe[3]
    if sjbh == '0' or iid == '0':
        return json.dumps('授权中，请稍等。。。', ensure_ascii=False)
    fk = selnoe[5]
    if '成功' in fk:
        return json.dumps('货件已完成，不允许重复建仓！', ensure_ascii=False)
    ret = mysql_xiugaifk(sjId)
    logger.info('{0}---{1}：---------------------执行结果---------------------'.format(dt_string, g.username))
    logger.info('{0}---{1}：反馈结果：{2}'.format(dt_string, g.username, ret))
    logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
    if ret:
        logger.info('{0}---{1}：执行成功！'.format(dt_string, g.username))
        return json.dumps('执行成功！', ensure_ascii=False)

    else:
        logger.info('{0}---{1}：执行失败！'.format(dt_string, g.username))
        return json.dumps('执行失败！', ensure_ascii=False)

@app.route('/xiugaisku', methods=['post'])
@login_required
def xiugaisku():
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    sjId = request.values.get('sjId')
    sku = request.values.get('sku')
    addr = request.values.get('addr')
    suocang = request.values.get('suocang')
    cx = mysql_cx(sjId)
    if cx:
        if '成功' in cx[0]:
            logger.info('{0}---{1}：不允许修改sku！---{2}'.format(dt_string, g.username, sjId))
            return json.dumps('不允许修改sku！', ensure_ascii=False)
        else:
            logger.info('{0}---{1}：允许修改sku！---{2}'.format(dt_string, g.username, sjId))

    logger.info('{0}---{1}：---------------------提交任务编号---------------------'.format(dt_string, g.username))
    logger.info('{0}---{1}：任务编号：{2}'.format(dt_string, g.username, sjId))
    logger.info('{0}---{1}：SKU：{2}'.format(dt_string, g.username, sku))
    logger.info('{0}---{1}：发货地址：{2}'.format(dt_string, g.username, addr))
    logger.info('{0}---{1}：锁仓：{2}'.format(dt_string, g.username, suocang))
    logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
    # if sjId == '' or sku == '' or addr == '' or suocang == '':
    #     return json.dumps('填写错误！', ensure_ascii=False)
    ret = mysql_xiugaisku(sjId, sku, addr, suocang)
    logger.info('{0}---{1}：---------------------执行结果---------------------'.format(dt_string, g.username))
    logger.info('{0}---{1}：反馈结果：{0}'.format(dt_string, g.username, ret))

    if ret:
        logger.info('{0}---{1}：修改成功！'.format(dt_string, g.username))
        logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
        return json.dumps('修改成功！', ensure_ascii=False)

    else:
        logger.info('{0}---{1}：修改失败！'.format(dt_string, g.username))
        logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
        return json.dumps('修改失败！', ensure_ascii=False)

@app.route('/zengjiahuojian', methods=['post'])
@login_required
def zengjiahuojian():
    '''新增货件'''
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    sjId = request.values.get('sjId')
    sku = request.values.get('sku')
    suocang = request.values.get('suocang')
    dqd = request.values.get('dqd')
    addr = request.values.get('addr')
    logger.info('{0}---{1}：---------------------增加货件---------------------'.format(dt_string, g.username))
    logger.info('{0}---{1}：任务编号：{2}'.format(dt_string, g.username, sjId))
    logger.info('{0}---{1}：SKU：{2}'.format(dt_string, g.username, sku))
    logger.info('{0}---{1}：锁仓：{2}'.format(dt_string, g.username, suocang))
    logger.info('{0}---{1}：多渠道：{2}'.format(dt_string, g.username, dqd))
    logger.info('{0}---{1}：发货地址：{2}'.format(dt_string, g.username, addr))
    logger.info('{0}---{1}：---------------------结束---------------------'.format(dt_string, g.username))
    if sjId == '' or sku == '' or suocang == '' or dqd == '':
        return 'null'
    selnoe = mysql_selnoe(sjId)
    if selnoe:
        rsjId = str(random.randint(100, 1000))+'-'+str(time.time())
        guojia = selnoe[0]
        cookie = selnoe[1]
        sjbh = selnoe[2]
        iid = selnoe[3]
        username = selnoe[4]
        zjhj = mysql_zengjiahuojian(rsjId, sku, suocang, guojia, cookie, sjbh, iid, dqd, username, addr)
        if zjhj:
            logger.info('{0}---{1}：编号：{2}，新增货件成功！：{3}'.format(dt_string, g.username, sjId, zjhj))
            return json.dumps('新增货件成功！:{0}'.format(rsjId), ensure_ascii=False)
        else:
            logger.info('{0}---{1}：编号：{2}，新增货件失败：{3}'.format(dt_string, g.username, sjId, zjhj))
            return json.dumps('新增货件失败！', ensure_ascii=False)
    else:
        logger.info('{0}---{1}：突破编号可能有误，{2}'.format(dt_string, g.username, sjId))
        return json.dumps('突破编号可能有误！', ensure_ascii=False)

# @app.route('/zz', methods=['get'])
# def zz():
#     print('zz')
#     return 'zz'







global logger
logger = Debug.logFrame().getlogger()
server = pywsgi.WSGIServer(('0.0.0.0', 55555), app)
server.serve_forever()



#server = pywsgi.WSGIServer(('localhost', 8000), app, allowed_hosts=['127.0.0.1', 'localhost'])




# if __name__ == "__main__":
#     global logger
#     logger = Debug.logFrame().getlogger()
#     app.run()
#     #app.run(host='0.0.0.0', port=55555, debug=True)
#     #WSGIServer(('0.0.0.0', 5002), app).serve_forever()
#     http_server = WSGIServer(('0.0.0.0', int(55553)), app)
#     http_server.serve_forever()