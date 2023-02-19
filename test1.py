#-- coding:utf-8 --



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from myimprot import Login as login
from myimprot import UpdateCookies as up
import string
import zipfile

from flask import request
import pymysql
'''
   突破授权
   '''


def jinrushouquan(driver, name, key):
    try:
        url = 'https://sellercentral.amazon.com/apps/manage/ref=xx_masman_dnav_xx'
        driver.get(url)
    except Exception as e:
        #print(222,e)
        driver.execute_script('window.stop()')
        return 0
    time.sleep(10)
    try:
        driver.find_element(By.XPATH, '//*[@id="mya-header-container"]/div[1]/kat-button/button').click()
    except Exception as e:
        print('登录错误')
        return 0
    time.sleep(10)
    #获取句柄
    windows = driver.window_handles
    #切换新窗口
    driver.switch_to.window(windows[-1])

    try:
        driver.find_element(By.XPATH, '//*[@id="developerInfo"]/div[1]/kat-input').send_keys(name)
        time.sleep(3)
        #//*[@id="katal-id-3"]
        driver.find_element(By.XPATH, '//*[@id="developerInfo"]/div[2]/kat-input').send_keys(key)
    except Exception as e:
        #//*[@id="errorContent"]/p[1]
        xysj = driver.find_element(By.XPATH, '//*[@id="errorContent"]/p[1]').text
        print(xysj)
        print(e)
        if xysj:
            return xysj, 0
        else:
            pass
    time.sleep(10)
    #//*[@id="navigationBar"]/kat-button/button
    #//*[@id="navigationBar"]/kat-button
    driver.find_element(By.XPATH, '//*[@id="navigationBar"]/kat-button').click()
    time.sleep(10)
    #//*[@id="root"]/div/div/div[3]/kat-checkbox
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[3]/kat-checkbox').click()
    time.sleep(10)
    #//*[@id="navigationBar"]/kat-button
    driver.find_element(By.XPATH, '//*[@id="navigationBar"]/kat-button').click()
    time.sleep(10)
    #//*[@id="root"]/div/div/h4[1]/b[2]      商家编号
    sjbh = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/h4[1]/b[2]').text
    #//*[@id="root"]/div/div/h4[3]/b[2]
    iid = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/h4[3]/b[2]').text
    print(sjbh, iid)

    return sjbh, iid

def create_proxyauth_extension(proxy_host, proxy_port,proxy_username, proxy_password,scheme='http', plugin_path=None):
        '''配置代理'''
        # 该配置不用改，可以直接用
        if plugin_path is None:
            plugin_path = 'chrome_proxyauth_plugin.zip'

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                      singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                      },
                      bypassList: ["foobar.com"]
                    }
                  };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )
        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

def mysql_xiugai(sjbh, iid, id, count):
    print(sjbh)
    print(iid)
    print(id)
    print(count[0][0])
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',
                           charset='utf8')
    cursor = conn.cursor()
    sql = ''
    if count[0][0] != '0':
        print('多渠道信息有数据')
        sql = r'update tp set zt = 1,sjbh=%s,iid=%s where id = %s'
    else:
        print('多渠道信息没有数据')
        sql = r'update tp set zt = 1,sjbh=%s,iid=%s,fk=1 where id = %s'
    try:
        ret = cursor.execute(sql, [sjbh, iid, id])
        if ret:
            print('授权添加数据成功！')
        else:
            print('授权添加数据失败！')
        conn.commit()
        return ret
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_xiugai1(fk,id):
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',charset='utf8')
    cursor = conn.cursor()
    sql = r'update tp set zt = 1,fk=%s where id = %s'
    try:
        ret = cursor.execute(sql, [fk, id])
        conn.commit()
        return ret
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_cx():
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon',charset='utf8')
    sql = r'select id,guojia,cookie from tp where zt = 0'
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        ret = cursor.fetchall()
        return ret
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def mysql_cx1(sjId):
    conn = pymysql.connect(host='43.142.154.185', port=3306, user='test01', passwd='zzzfsg3574.', db='amazon', charset='utf8')
    sql = r'select dqd from tp where id = %s'
    cursor = conn.cursor()
    try:
        cursor.execute(sql, sjId)
        ret = cursor.fetchall()
        return ret
    except Exception as e:
        print(e)
        return 0
    finally:
        cursor.close()
        conn.close()

def run(cookie,guojia,id):
    '''授权'''
    #cookie = r'[{"domain":".amazon.com","expirationDate":1704783102,"hostOnly":false,"httpOnly":true,"name":"at-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"Atza|IwEBII3DB6CPs1X9bzEjZYdHfbjlzdjEbnXN7Q_Kcmzoh0J2Im2VIvUVZlryijLjyhtC8jWj9tLYIsIlWqL4z4XXNlJfMJy7_iW-__VSFWmCK7vUKNs4D4iZYl2MVsRbjFzEoau0itwqI9Zjjlp-YPX_28ekml2oP_FfJ_TWTr2LQIXUnECL0lGsEBCA19Js0V5MkmVQL3PmDwBMwO5DW0jfRlA2L6mD2RJstf7-xhVhA6EUFg","id":1},{"domain":".amazon.com","expirationDate":1703902155,"hostOnly":false,"httpOnly":false,"name":"i18n-prefs","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"USD","id":2},{"domain":".amazon.com","expirationDate":1831013496,"hostOnly":false,"httpOnly":false,"name":"s_pers","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"%20s_fid%3D77D6DB06E756C87C-2C60703555893BCC%7C1831013496364%3B%20s_dl%3D1%7C1673248896364%3B%20s_ev15%3D%255B%255B%2527SCUSWPDirect%2527%252C%25271672037096012%2527%255D%252C%255B%2527Typed%252FBookmarked%2527%252C%25271672366064785%2527%255D%252C%255B%2527SCUSWPDirect%2527%252C%25271673247096366%2527%255D%255D%7C1831013496366%3B","id":3},{"domain":".amazon.com","expirationDate":1704783102,"hostOnly":false,"httpOnly":true,"name":"sess-at-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"\"vErNeCfOo1Keh1ivDvdzF23ACIu6o36psQF5kev3dD4=\"","id":4},{"domain":".amazon.com","expirationDate":1704783102,"hostOnly":false,"httpOnly":false,"name":"session-id","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"135-8329449-6465617","id":5},{"domain":".amazon.com","expirationDate":1704783102,"hostOnly":false,"httpOnly":false,"name":"session-id-time","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"2303967101l","id":6},{"domain":".amazon.com","expirationDate":1704794573.022258,"hostOnly":false,"httpOnly":false,"name":"session-token","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"SI6N+lBDYmiVDCKoUymVpepxvafvZtDHRQDcRmJEhDmzfzcgQWw3CNFAMS0lHdYUWfqpFmp34FXphlMhcPTA3k0GpS9poK6K4WKX0zFtq9THeX70vSPOlJZT+bD4nPRYxwQrE2BATdc/eeBIaXKeJnASz3GBq+yYW60Bf41KUShcCBf8OImuyhuNJs/Y+LQOaIsR5QCjUVScv5UfKXcxOMudpZcLHMY1q/w8UXEyNCW2/SG5FtRNkJVHAeKtSm3J","id":7},{"domain":".amazon.com","expirationDate":1697687538,"hostOnly":false,"httpOnly":true,"name":"sid","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"\"Oc0+wvmOc2qHP6Ox5BidsQ==|Hnp17rpsty7TVcwacezCJUVzGmem6TS72ubnq793moA=\"","id":8},{"domain":".amazon.com","expirationDate":1704783102,"hostOnly":false,"httpOnly":true,"name":"sst-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"Sst1|PQEycYI-A44KbuDBOayb_gcqCS2SfaNu0S26m5aruThmmwYq5esIjWU5bxto35cLb2ZhkTtztjYDfUHeKXWM78UL8CcV87ZuGwfhZhoKB-oaApOS7cK00q89pCiQ2Dc_3SAfQopDpp7i3WJLenZPv0tpaEft9XNch8Zl4FT5SjVZcClWyriEMhnH6u6EM8YPqSQxycYdn7T8mr5I-libC2GAogzchvGaF77Wiv-KNGLshP_WTrL9G-tpow6gAYwGh5vKVzitHqTIkqZrlaBNaNyJH6VoUDOYZYKI8L_koqAiP8A","id":9},{"domain":".amazon.com","expirationDate":1704783102,"hostOnly":false,"httpOnly":false,"name":"ubid-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"134-1555884-3998434","id":10},{"domain":".amazon.com","expirationDate":1704783102,"hostOnly":false,"httpOnly":false,"name":"x-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"\"ehAYGbW@u0@gStyZRBy9aKploKnh5R?4pKVIIA1zjK@EYxEvmNXGU76BaBEOY4E1\"","id":11},{"domain":"sellercentral.amazon.com","expirationDate":1702610282,"hostOnly":true,"httpOnly":true,"name":"__Host_mlang","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"zh_CN","id":12},{"domain":"sellercentral.amazon.com","expirationDate":1702627555,"hostOnly":true,"httpOnly":true,"name":"__Host-mselc","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"H4sIAAAAAAAA/6tWSs5MUbJSSsytyjPUS0xOzi/NK9HLT85M0XM09oiwDIpwd7GwdHYyVdJRykVSmZtalJyRCFKKRV02ssICkJKQsAAXb0/vCAMX1yClWgDpm9J3dQAAAA==","id":13},{"domain":"sellercentral.amazon.com","expirationDate":1703487101,"hostOnly":true,"httpOnly":false,"name":"csm-hit","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"tb:44YDVW700ZBHK22ZGAY3+s-4BKAW6M906CFS08X2Y8G|1673247101412&t:1673247101412&adb:adblk_no","id":14},{"domain":"sellercentral.amazon.com","expirationDate":1674514270,"hostOnly":true,"httpOnly":false,"name":"ld","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"SCUSWPDirect","id":15}]'
    #guojia = '美国'
    dqsj = time.time()
    name = 'TP_{0}'.format(dqsj)
    #开发者账号
    key = '388105496607'

    # s = Service("chromedriver.exe")
    opt = Options()
    # opt.add_argument("--headless")
    # opt.add_argument("--disbale-gpu")
    # opt.add_argument("blink-settings=imagesEnabled=false")
    opt.add_argument(
    '--user-agent=Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36')
    opt.add_argument('--start-maximized')
    opt.add_argument('--disable-infobars')
    # proxyauth_plugin_path = create_proxyauth_extension(
    #     proxy_host="zproxy.lum-superproxy.io",
    #     proxy_port=22225,
    #     # proxy_username="lum-customer-hl_4b189e27-zone-zoneemail-session-{0}".format(count)
    #     # lum-customer-hl_4b189e27-zone-zoneemail
    #     proxy_username="brd-customer-hl_f8213931-zone-zonetest-country-us",
    #     proxy_password="w123456d"  # email11111111
    # )
    # opt.add_extension(proxyauth_plugin_path)
    driver = webdriver.Chrome(options=opt)
    cookies = up.update_cookies_json(cookie)
    bo = True
    while bo:
        ret = login.login_chrome_amazon_seller(driver, cookies, guojia)
        if ret:
            bo = False
        time.sleep(2)
    sjbh,iid = jinrushouquan(driver, name, key)
    driver.close()
    return sjbh,iid,id




if __name__ == '__main__':

    '''店铺授权'''
    while True:
        try:
            cx = mysql_cx()

            if cx:
                #cx[0][1]
                guojia = ''
                if cx[0][1] == 'US':
                    guojia = '美国'
                elif cx[0][1] == 'CA':
                    guojia = '加拿大'
                else:
                    xiugai1 = mysql_xiugai1('暂不支持除美国和加拿大以外的站点', cx[0][0])
                    print('id:{0},暂不支持除美国和加拿大外的站点'.format(cx[0][0]))
                    continue
                sjbh, iid, id = run(cx[0][2], guojia, cx[0][0])
                if iid == 0: #判断没获取到授权码则直接修改反馈
                    xiugai1 = mysql_xiugai1(sjbh, id)
                    continue
                #判断：如果多渠道信息为0则执行
                count = mysql_cx1(id)
                xiugai = mysql_xiugai(sjbh, iid, id, count)
                print('执行：{0}，id：{1}'.format(xiugai, cx[0][0]))
                time.sleep(10)
            else:
                print('授权没找到需要发送的数据！')
                time.sleep(30)
        except Exception as e:
            print(e)
            time.sleep(10)
            continue


    #梯子问题
    #pip install urllib3==1.25.11




