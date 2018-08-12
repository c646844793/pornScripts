# coding:utf-8


import os
from bs4 import BeautifulSoup
import requests

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
headers = {
    "Host": "t66y.com",
    "Accept-Encoding": "gzip, deflate",
    'User-Agent': agent,
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
}
pre = "http://t66y.com/"


def judge_url():
    urldic = {}
    if os.path.exists("photo_url.txt"):
        if os.path.getsize("photo_url.txt") > 0:
            f = open('photo_url.txt', 'r', encoding="utf-8")
            for line in f:
                line = line.strip('\n')
                key, value = line.split("=", 1)
                urldic[key] = value
            f.close()
    else:
        f = open('photo_url.txt', 'w')
        f.close()
    url = "http://t66y.com/thread0806.php?fid=16&search=&page=1"
    html = requests.get(url, headers=headers)
    html.encoding = 'gbk'
    soup = BeautifulSoup(html.text, "html.parser")
    lines = soup.find_all('tr', class_="tr3 t_one tac")
    for line in lines:
        a_all = line.find_all('a')
        urltd = a_all[0]
        url_cut = urltd['href'].split('/')
        if urltd['href'] in urldic.keys():
            continue
        # 不存在字典里，即没有被下载过，且页数大于15，才允许下载
        if len(url_cut) == 4:
            # 非无关广告贴 大于18年七月
            if int(url_cut[2]) > 1807:
                last_page = a_all[len(a_all) - 3].string
                if is_number(last_page) and int(last_page) > 15:
                    saveHtmlAndPhoto(urltd['href'], a_all[1].string)
                    urldic[urltd['href']] = a_all[1].string
    fp = open('photo_url.txt', 'w', encoding="utf-8")
    for x in urldic:
        line = x + '=' + urldic[x]
        fp.write(line)
        fp.write('\n')  # 显示写入换行
    fp.close()


def saveHtmlAndPhoto(post_url, post_name):
    post_name = str(post_name)
    html = requests.get(pre + post_url, headers=headers)
    html.encoding = 'gbk'
    soup = BeautifulSoup(html.text, "html.parser")
    # pics = soup.find_all(type='image')
    # index = 1
    # for i in pics:
    #     photo_url = i["data-src"]
    #     photo_data = requests.get(photo_url).content
    #     temp = photo_url.split('.')
    #     suffix = temp[len(temp)-1]
    #     with open("1024photo/"+post_name+"/"+str(index) + "." + suffix, "w+") as handler1:
    #         handler1.write(photo_data)
    #         i["src"] = str(x) + "-" + str(index) + "." + suffix
    with open("1024photo/" + post_name + ".html", "w",  encoding="utf-8") as handler:
        handler.write(str(soup))


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    judge_url()
