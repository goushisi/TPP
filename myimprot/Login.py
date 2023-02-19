# -*- coding: utf-8 -*-
# @Author:S
# @Time    : 2022/7/27 21:44
'''
登陆

'''
from selenium.webdriver.common.by import By
import time
from myimprot import UpdateCookies as uc
from selenium.common.exceptions import NoSuchElementException

def login_chrome_amazon_seller(driver, cookies, nation):
        print(nation)
        '''模拟谷歌浏览器登陆亚马逊卖家店铺,登陆成功返回1否则返回0'''
        driver.set_page_load_timeout(20)  # 页面加载超时时间
        driver.set_script_timeout(20)  # 页面js加载超时时间
        yu = uc.getcookieyu(cookies)
        url = 'https://{0}/'.format(yu)
        print(yu)
        print(url)
        try:
            print('程序进行中。。。')
            # 请求网页
            driver.get(url)
            # 删除当前页面所有cookie
            driver.delete_all_cookies()
            # 刷新
            driver.refresh()
            # 导入cookie
            for cookie in cookies:
                # 获取当前cookie的index
                cookie_index = cookies.index(cookie)
                # 删除name=__Host-mselc的这条cookie
                if cookie['name'] == '__Host-mselc':
                    cookies.pop(cookie_index)
                    continue
                cookie["sameSite"] = "Strict"
                # if cookie['name']  == 'sst-main':
                driver.add_cookie(cookie)
            # 再次请求网页
            driver.get(url)
        except Exception as e:
            print('1111', e)
            driver.execute_script('window.stop()')
            return 0
        num_1 = 20
        while True:
            try:
                # 判断为True则为获取到密码框说明登陆失败反馈0
                # 获取密码框
                # //*[@id="ap_password"]
                pwd = driver.find_element(By.XPATH, '//*[@id="ap_password"]')
                # //*[@id="sc-content-container"]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/a
                if pwd:
                    print('请更换节点尝试。。。')
                    return 0
            except Exception as e:
                print('没检测到密码框！正常通行！')
            try:
                #检测登陆界面
                # //*[@id="sc-content-container"]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/a
                container = driver.find_element(By.XPATH,'//*[@id="sc-content-container"]/div/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/a').text
                if container:
                    print('请更换节点尝试。。。')
                    return 0
            except Exception as e:
                print('没检测到登陆界面！正常通行！')


            try:
                time.sleep(2)
                #//*[@id="picker-container"]/div/div[1]/div/div
                yw = driver.find_element(By.XPATH, '//*[@id="picker-container"]/div/div[1]/div/div').text
                print(yw)
                if 'Account' in yw:
                    print(11111111111111111)
                    if nation == '美国':
                        print(222222222222222222)
                        nation = 'United States'
                    elif nation == '加拿大':
                        nation = 'ca'
                    else:
                        print(44444444444444444444444)
                else:
                    print(333333333333)
                # 获取站点列表
                nations = driver.find_elements(By.XPATH,'//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div')
            except Exception as e:
                print('没有获取到站点信息', e)
                continue
            try:
                for zd in nations:
                    #当前站点与输入站点一致时则点击选中此站点并提交
                    print('tjzd:',nation)
                    print('当前站点:{0}'.format(zd.text))
                    if zd.text == nation:
                        print('站点对于上！')
                        #选中站点再下滑10px保证完全获取数据
                        #js = "document.getElementsByClassName('picker-view-column')[2].scrollTop = 10"
                        #driver.execute_script(js)
                        zd_index = nations.index(zd)+1
                        time.sleep(2)
                        try:
                            # 选中当前站点
                            # //*[@id="picker-container"]/div/div[2]/div/div[3]/div/div[7]/button
                            driver.find_element(By.XPATH,'//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div[{0}]/button'.format(zd_index)).click()
                            print('已选择当前站点')
                            # 选中站点点击提交
                            driver.find_element(By.XPATH,'//*[@id="picker-container"]/div/div[3]/div/button').click()
                            return 1
                        except Exception as e:
                            print('站点选择报错！')
                            continue
                    else:
                        print(num_1)
                        print('未选中站点信息！')
                        # 未选中站点则下滑列表框，重新执行

                        js = "document.getElementsByClassName('picker-view-column')[2].scrollTop = {0}".format(num_1)
                        js1 = '''
                            function getScrollTop() {
                              let scroll_top = 0;
                              if (document.documentElement && document.documentElement.scrollTop) {
                                scroll_top = document.documentElement.scrollTop;
                              } else if (document.body) {
                                scroll_top = document.body.scrollTop;
                              }
                              return scroll_top;
                            }
                        '''
                        driver.execute_script(js)
                num_1 = num_1 + 20
            except Exception as e:
                print(e)
                continue





def login_chrome_amazon_buyer(cookies,driver):
    '''模拟谷歌浏览器登陆亚马逊买家后台'''
    yu = uc.getcookieyu(cookies)
    print(yu)
    url = 'https://{0}/'.format(yu)
    print('url:', url)
    try:
        # 请求网页
        driver.get(url)
        # 删除当前页面所有cookie
        driver.delete_all_cookies()
        # 刷新
        driver.refresh()
        # 导入cookie
        for cookie in cookies:
            print('注入cookie:', cookie)

            cookie["sameSite"] = "Strict"
            # if cookie['name']  == 'sst-main':
            driver.add_cookie(cookie)
        time.sleep(3)
        driver.get(url)
    except Exception as e:
        print(e)



