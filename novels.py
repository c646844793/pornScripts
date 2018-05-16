#!/usr/bin/python
# coding=utf-8

import requests
import re
import os
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
import multiprocessing


def process(pagenum, x):
    #http://sis001.us/forum/forum-383 代表原创人生区小说
    base_url = 'http://sis001.us/forum/forum-383-%d.html'
    wanted = []
    for i in range(pagenum, pagenum+10):
        r = requests.get(base_url % i)

        r.encoding = 'gbk'
        html = r.text

        soup = BeautifulSoup(html, "html.parser")
        for line in soup.find_all(id=re.compile("^normalthread")):
            if line is not None:
                comments = line.find('strong')
                if comments is not None:
                    if comments.string.isdigit() and int(comments.string) >= 100:
                        span = line.find(id=re.compile("^thread"))
                        if not span.contents[0].string:
                            continue
                        wanted.append({'link': 'http://sis001.com/forum/' + span.contents[0].get('href'),
                                       'text': span.contents[0].string})

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(THIS_DIR))
    template = env.get_template('template/sis.template')

    content = template.render(wanted=wanted)

    filename = 'template/sisNovels-100-%d.html'
    fp = open(filename % (x+1), 'w', encoding="utf-8")
    fp.write(content)
    fp.close()

#多进程提高方法执行速度
if __name__ == '__main__':
    #需要爬取的页码数，从第1到第141页
    for i in range(0, 13):
        j = i * 10 + 1
        p = multiprocessing.Process(target=process, args=(j, i,))
        p.start()
