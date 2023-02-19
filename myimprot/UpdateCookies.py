# -*- coding: utf-8 -*-
# @Author:S
# @Time    : 2022/7/27 21:34

'''
cookie 处理
'''


def update_cookies_json(cookies) :
        '''处理json格式cookie返回cookie'''

        # cookie = r'[{"domain":".amazon.com","expirationDate":1688463384.106,"hostOnly":false,"httpOnly":true,"name":"at-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"Atza|IwEBIBvfk7l7s-XJKvWuQ-paddfUwp9R5hKOnVmwvYqgIgQZenjUg2daC4iwrSrTsaXBR8zjTOYniVixXECIlsFriHG9XaXpNeCFcQUX-73l1kBxUtHJgYNAbmWnn8dUhowlUfHxBV3mkjZ0-0PsQJ2EsCbF3tHrLVIwppIffYhEb5YzurY7G6dw-CUcCa_0wF5G81NnWrksn9ScbYBinzjR5tVnykt7XIOphh6icl-nU_KEUA","id":1},{"domain":".amazon.com","expirationDate":1688660004.544002,"hostOnly":false,"httpOnly":false,"name":"i18n-prefs","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"USD","id":2},{"domain":".amazon.com","expirationDate":1814693766,"hostOnly":false,"httpOnly":false,"name":"s_pers","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"%20s_fid%3D56A06C4C5B7FBBF4-09806DF390A734B2%7C1814693766762%3B%20s_dl%3D1%7C1656929166763%3B%20s_ev15%3D%255B%255B%2527Typed%252FBookmarked%2527%252C%25271656408949494%2527%255D%252C%255B%2527ASUSWPDirect%2527%252C%25271656927366769%2527%255D%255D%7C1814693766768%3B","id":3},{"domain":".amazon.com","expirationDate":1688463384.106,"hostOnly":false,"httpOnly":true,"name":"sess-at-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"\"Ro8Al71suQgJsljGAVl2TRxUVjU+p2sHirU6YG2ROHo=\"","id":4},{"domain":".amazon.com","expirationDate":1688660032.912002,"hostOnly":false,"httpOnly":false,"name":"session-id","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"145-9160752-7297756","id":5},{"domain":".amazon.com","expirationDate":1684379160.181,"hostOnly":false,"httpOnly":false,"name":"session-id-eu","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"258-7861298-5066505","id":6},{"domain":".amazon.com","expirationDate":1688444249.314,"hostOnly":false,"httpOnly":false,"name":"session-id-jp","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"356-2395642-3386005","id":7},{"domain":".amazon.com","expirationDate":1688660032.912002,"hostOnly":false,"httpOnly":false,"name":"session-id-time","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"2082787201l","id":8},{"domain":".amazon.com","expirationDate":1684379160.181,"hostOnly":false,"httpOnly":false,"name":"session-id-time-eu","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"2283563158l","id":9},{"domain":".amazon.com","expirationDate":1688444249.314,"hostOnly":false,"httpOnly":false,"name":"session-id-time-jp","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"2287628250l","id":10},{"domain":".amazon.com","expirationDate":1688867129.124152,"hostOnly":false,"httpOnly":false,"name":"session-token","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"qWlVoU7oDZELOF7Yu2iQRMVjcAoXOTH39UCOIEy8SXMn9zB78I2TBSefaLzjDbIzWDjm09Hvvx/E+wKsceSAqrFXIOQKsUUw/VlbzFEaai1OwfOCw5eKf1VJ/wPN62ozmbUoIHwTQylzW0UyNag+gTsqhgB0b0n6uWhFOZEk+Bkt7JmtYhRUPwOxoUKX07Xk0Yfb2vkDWPQXaokoyF+bpJsbI70H22Gz","id":11},{"domain":".amazon.com","expirationDate":1668674708.084,"hostOnly":false,"httpOnly":true,"name":"sid","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"\"YqCwcyUpprRUMpaRqxU4JA==|xksYyXxgjxHdnXUVoCGAhbTBkHsBGU0WRJy49Wd+R1Y=\"","id":12},{"domain":".amazon.com","expirationDate":1688463384.106,"hostOnly":false,"httpOnly":true,"name":"sst-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"Sst1|PQGqB1jrQcQ9ApQ7I4ycIhTyCQNTzdIBukqtlM58jjRZUlU7v0qnYXSMYdFGFx150DRicca4gcSsU4OYyjHXfPnMAci-2ZMLaAQh7K6Fc9zfCNLbQEOibMC2bHwU-VkBC55OhNv3A4-u7Nqkhya7dFqhXaQ-bq-nkzXkdtTDITdwqxmo4w-jjQJAjBYy25wd8fi1u28WDAVT4qDyAAGT-GVkeQ5UH5bvKpD8GToWEqogjGmTvzaF7q7CqvxCO5mrvE3lN-R0JGJRCErPpE68JEKFjfWe0H6JmDO9lB9Cp_3XIrs","id":13},{"domain":".amazon.com","expirationDate":1688444249.314,"hostOnly":false,"httpOnly":false,"name":"ubid-acbjp","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"356-9008963-0860108","id":14},{"domain":".amazon.com","expirationDate":1684379160.181,"hostOnly":false,"httpOnly":false,"name":"ubid-acbuk","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"262-1901931-8559612","id":15},{"domain":".amazon.com","expirationDate":1688660032.911,"hostOnly":false,"httpOnly":false,"name":"ubid-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"135-1057666-4316262","id":16},{"domain":".amazon.com","expirationDate":1684379160.182,"hostOnly":false,"httpOnly":false,"name":"x-acbuk","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"x8Kvs5oEGny9qVwU7gLeUum69kHnWbcaCmxsFQnfxPueQiZVJsvHouuYK77Y38nC","id":17},{"domain":".amazon.com","expirationDate":1688660004.544002,"hostOnly":false,"httpOnly":false,"name":"x-main","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"\"YElHyDnmzmAFOXdh1OxsSgf?hVcDWWC1Ty4oQAiuDbDWon6mp50Axc1xSPHereP0\"","id":18},{"domain":"sellercentral.amazon.com","expirationDate":1688679461.257,"hostOnly":true,"httpOnly":true,"name":"__Host_mlang","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"zh_CN","id":19},{"domain":"sellercentral.amazon.com","expirationDate":1688442981.284002,"hostOnly":true,"httpOnly":true,"name":"__Host-mselc","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"H4sIAAAAAAAA/6tWSs5MUbJSSsytyjPUS0xOzi/NK9HLT85M0XM0MgxwCTEyNXD29fB1U9JRykVSmZtalJyRCFKKRV02ssICkJKQsAAXb0/vCAMX1yClWgAlXhwcdQAAAA==","id":20},{"domain":"sellercentral.amazon.com","expirationDate":1687167382,"hostOnly":true,"httpOnly":false,"name":"csm-hit","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"tb:CJSAE7GWP8S0Y88FMYQF+s-G9VT0TTDG59AXJG5H13H|1656927382560&t:1656927382560&adb:adblk_no","id":21},{"domain":"sellercentral.amazon.com","expirationDate":1658198166,"hostOnly":true,"httpOnly":false,"name":"ld","path":"/","sameSite":"unspecified","secure":false,"session":false,"storeId":"0","value":"ASUSWPDirect","id":22},{"domain":"sellercentral.amazon.com","expirationDate":1657729027.959,"hostOnly":true,"httpOnly":true,"name":"stck","path":"/","sameSite":"unspecified","secure":true,"session":false,"storeId":"0","value":"NA","id":23}]'
        # print(cookie)
        # 将cookie中的所有true变成True
        cookies = cookies.replace('true', 'True')
        ##将cookie中的所有false变成False
        cookies = cookies.replace('false', 'False')
        cookies = cookies.replace('Name', 'name')
        cookies = cookies.replace('Domain', 'domain')
        # 去除前后中括号
        cookies = cookies[1:-1]
        cookies_ = []
        # 通过 },截取
        a = cookies.split('},')
        for i in a:
            # 判断字符串结尾没有‘}’则添加}
            if i[-1] != '}':
                i = i + '}'
            # 将字符串转为json格式
            c = eval(i)

            cookies_.append(c)
        return cookies_

def getcookieyu(cookie):
    yu = ''
    for ck in cookie:
        yu = ck['domain']
    # if 'www' in yu:
    #     return yu
    # else:
    #     return 'www'+yu
    return yu


