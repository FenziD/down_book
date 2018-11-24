from bs4 import BeautifulSoup
import requests
import json
import random
import time
from spider import myipAgent

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
}
cookie = {}

def choiceIP(ip_pool):
    ip=random.choice(ip_pool)
    proxy={'http':ip,'https':ip}
    return proxy

def getSessionid():
    login_url = 'http://cn.epubee.com'
    req = requests.get(login_url, headers=headers)
    str = req.headers['Set-Cookie']
    name, value = str.split(';')[0].split('=')
    return value


def getCookie(proxy):
    print('开始获取cookie')
    cookie['ASP.NET_SessionId'] = getSessionid()
    url = 'http://cn.epubee.com//keys/genid_with_localid.asmx/genid_with_localid'
    data = {'localid': ''}

    # try:
    #     response = requests.post(url, json=data, cookies=cookie, proxies=proxy)
    #     data = (json.loads(response.content.decode()))['d'][0]
    #     cookie['identify'] = data.get('ID')
    #     cookie['identifyusername'] = data.get('UserName')
    #     cookie['user_localid'] = data.get('Name')
    #     cookie['uemail'] = data.get('email')
    #     cookie['kindle_email'] = data.get('kindle_email')
    #     cookie['isVip'] = '1'
    #     cookie['leftshow']='1'
    # except:
    #     print("获取cookie失败！")

    response = requests.post(url, json=data, cookies=cookie, proxies=proxy)
    data = (json.loads(response.content.decode()))['d'][0]
    cookie['identify'] = data.get('ID')
    cookie['identifyusername'] = data.get('UserName')
    cookie['user_localid'] = data.get('Name')
    cookie['uemail'] = data.get('email')
    cookie['kindle_email'] = data.get('kindle_email')
    cookie['isVip'] = '1'
    cookie['leftshow']='1'


def cookie_toString(cookie):
    cookie_str=''
    for name,vlaue in cookie.items():
        cookie_str=cookie_str+str(name)+'='+str(vlaue)+'; '
    return cookie_str

def add_Book(cookie, bookid, proxy):
    print('开始加入书本')
    uid = cookie.get('identify')
    cookie_str = cookie_toString(cookie)
    act = 'search'
    url = 'http://cn.epubee.com/app_books/addbook.asmx/online_addbook'
    data = {'bookid': bookid, 'uid': uid, 'act': act}
    header = {
        'Host': 'cn.epubee.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/json',
        'Cookie': cookie_str,
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive'
    }
    # try:
    #     response = requests.post(url,headers=header,json=data,proxies=proxy)
    #     if response.status_code!=200:
    #         print('书本加入失败')
    #     else:
    #         print('书本加入成功')
    # except:
    #     print('书本加入失败\n')

    response = requests.post(url, headers=header, json=data, proxies=proxy)
    if response.status_code != 200:
        print('书本加入失败')
    else:
        print('书本加入成功')


def getBookList(cookie,proxy):
    print('开始获取书本下载地址')
    uid = str(cookie.get('identify'))
    url = 'http://cn.epubee.com/files.aspx?userid=' + uid
    cookie_str = cookie_toString(cookie)
    header = {
        'Host': 'cn.epubee.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': cookie_str,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'max-age=0 ',
    }
    # try:
    #     req = requests.get(url, headers=header,proxies=proxy)
    #     if req.status_code==200:
    #         bsObj = BeautifulSoup(req.text, 'html.parser')
    #         name_0 = bsObj.find('span', {'id': 'gvBooks_lblTitle_0'}).get_text()
    #         format_0 = bsObj.find('a', {'id': 'gvBooks_gvBooks_child_0_hpdownload_0'}).get_text()
    #         filename = name_0 + format_0
    #         bid = bsObj.find('span', {'id': 'gvBooks_gvBooks_child_0_lblBID_0'}).get_text()
    #         return filename, bid
    #     else:
    #         print('fail')
    #         return
    # except:
    #     print('fail')
    #     return

    req = requests.get(url, headers=header, proxies=proxy)
    if req.status_code == 200:
        bsObj = BeautifulSoup(req.text, 'html.parser')
        name_0 = bsObj.find('span', {'id': 'gvBooks_lblTitle_0'}).get_text()
        format_0 = bsObj.find('a', {'id': 'gvBooks_gvBooks_child_0_hpdownload_0'}).get_text()
        filename = name_0 + format_0
        bid = bsObj.find('span', {'id': 'gvBooks_gvBooks_child_0_lblBID_0'}).get_text()
        return filename, bid
    else:
        print('fail')
        return


def gett_key(bid,proxy):
    url = 'http://cn.epubee.com/app_books/click_key.asmx/getkey'
    data = {'isVip': 1, 'uid': cookie.get('identify'),'strbid': bid}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data,proxies=proxy)
    dict = json.loads(response.content.decode())
    t_key=dict.get('d')[0]
    return t_key


def download(filename, bid, cookie,loc,proxy):
    filename = loc + filename
    cookie_str = cookie_toString(cookie)
    uid = str(cookie.get('identify'))
    t_key = gett_key(bid,proxy)
    url = 'http://cn.epubee.com/getFile.ashx?bid=' + bid + '&uid=' + uid + '&t_key=' + t_key
    header = {
        'Host': 'cn.epubee.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Cookie': cookie_str,
        'Upgrade-Insecure-Requests': '1',
    }
    down = requests.get(url, headers=header,proxies=proxy)
    with open(filename, 'wb')as code:
        code.write(down.content)

# def getSearchList(proxy):
#
#     url='http://cn.epubee.com/keys/get_ebook_list_search.asmx/getSearchList'
#     data={'skey':'python'}
#     cookie_str = cookie_toString(cookie)
#     header = {
#         'Host': 'cn.epubee.com',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.5',
#         'Accept-Encoding': 'gzip, deflate',
#         'Cookie': cookie_str,
#         'Upgrade-Insecure-Requests': '1',
#     }
#     response = requests.post(url,headers=header,json=data, proxies=proxy)
#     print(response.status_code)
#     dict = json.loads(response.content.decode())['d']
#     print(len(dict))



if __name__ == '__main__':

    path = 'ip.txt'  # 存放爬取ip的文档path
    with open(path, 'r+') as f:
        iplist = f.readlines()
    for i in range(0, len(iplist)):
        iplist[i] = iplist[i].strip('\n')

    # loc=input("请输入存放地址：")
    loc='F:\\资料\\电子书\\kindle\\'

    # 下载地址---F:\资料\电子书\kindle\   KxrbnqbpG9yIpkxWSozxtw%3d%3d
    while(True):

        try:
            ip = random.choice(iplist)
            proxy={'http':ip,'https':ip}
            print('代理IP: %s', proxy.get('http'))
            getCookie(proxy)
            uid = str(cookie.get('identify'))
            print('用户：', uid)
            time.sleep(1)
            bookid = str(input('请输入：'))
            add_Book(cookie, bookid,proxy)
            time.sleep(3)
            filename, bid = getBookList(cookie,proxy)
            print('开始下载', filename)
            download(filename,bid,cookie,loc,proxy)
            print('done!')
        except:
            str=input('请输入Ent继结束操作,按c继续')
            print('ip：%s不可用',(ip))
            if str=='\n':
                break
            elif str.lower()=='c':
                continue
            else:
                break

    # 获取图书测试
    # ip = random.choice(iplist)
    # proxy={'http':ip,'https':ip}
    # print('代理IP: %s', proxy.get('http'))
    # getCookie(proxy)
    # uid = str(cookie.get('identify'))
    # print('用户：', uid)
    # time.sleep(1)
    # input('en')
    # getSearchList(proxy)


