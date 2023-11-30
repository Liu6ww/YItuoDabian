# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm
from time import sleep

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
'''
    User-Agent头部字段通常用于服务器识别请求来源的客户端信息，包括操作系统、浏览器类型、浏览器版本等。
    一些网站会根据这些信息提供不同的服务，例如移动版和桌面版的网页。
    有些网站甚至会阻止没有User-Agent或User-Agent不符合特定模式的请求，以防止爬虫抓取数据。
因此，如果不添加这个header，可能会遇到一些问题，如请求被拒绝、获取到的数据与预期不符等。
    '''


def crawl_lianjia():
    '''
    这个函数用于爬取链家网站的租房信息。
    首先定义了一个URL模板，然后打开一个CSV文件用于写入数据。
    使用一个带有进度条的循环来遍历页面。
    对于每个页面，发送一个GET请求，然后解析返回的HTML。
    如果找到了需要的信息，就将其写入CSV文件。
    '''
    url = 'https://sh.lianjia.com/zufang/pg{page}/'
    csv_file = open('lianjia.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    print('start fetch linjia..')
    for i in tqdm(range(1, 101)):
        sleep(1)
        '''
        使程序在每次请求页面之间暂停1秒，目的是为了防止对服务器的过度请求，因为过度请求可能会导致IP地址被服务器封锁。
        通过在请求之间添加适当的延迟，可以模拟人类用户的行为，降低被封锁的风险。
        '''
        response = requests.get(url.format(page=i), headers=header, allow_redirects=False)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'lxml')
            for item in html.select('.info-panel'):
                houseUrl = item.find('h2').a['href']
                title = item.find('h2').a['title']
                location = title.split(' ')[0]
                csv_writer.writerow([title, location, houseUrl])
        else:
            break
        '''
        遍历HTML文档中所有的.info-panel元素。对于每个元素，它都会找到第一个h2标签下的a标签，然后从这个a标签的href属性中提取出房源的URL，
        从title属性中提取出标题。然后，它会将标题按空格分割，取出第一个部分作为位置。最后，它将标题、位置和房源的URL写入CSV文件。
        '''


def crawl_anjuke():
    url = 'https://sh.zu.anjuke.com/fangyuan/p1/'
    csv_file = open('anjuke.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    print('start fetch anjuke..')
    print('fetching anjuke..')
    while True:
        sleep(1)
        response = requests.get(url, headers=header, allow_redirects=False)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'lxml')
            try:
                url = html.select('.aNxt')[0]['href']
            except:
                url = None
            for item in html.select('.zu-itemmod .zu-info'):
                houseUrl = item.find('h3').a['href']
                title = item.find('h3').a['title']
                try:
                    location = item.address.a.string
                except:
                    location = None
                if location:
                    csv_writer.writerow([title, location, houseUrl])
            if not url:
                break
        else:
            break


def crawl_58():
    url = 'http://sh.58.com/chuzu/pn{page}/'
    csv_file = open('58tongcheng.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    print('start fetch 58 tongcheng..')
    for i in tqdm(range(1, 71)):
        sleep(1)
        response = requests.get(url.format(page=i), headers=header, allow_redirects=False)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'lxml')
            for item in html.select('li .des'):
                houseUrl = item.find('h2').a['href']
                title = item.find('h2').a.string.strip()
                try:
                    locations = item.select('.add')[0].find_all('a')
                    location = locations[0].string + ' ' + locations[1].string
                except:
                    location = None
                if location:
                    csv_writer.writerow([title, location, houseUrl])
            if not url:
                break
        else:
            break


def crawl_ganji():
    url = 'http://sh.ganji.com/fang1/o1/'
    prefix = 'http://sh.ganji.com'
    csv_file = open('ganji.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    print('start fetch ganji..')
    print('fetching ganjiwang..')
    while True:
        sleep(1)
        response = requests.get(url, headers=header, allow_redirects=False)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'lxml')
            try:
                url = prefix + html.select('.next')[0]['href']
            except:
                url = None
            for item in html.select('.f-list-item .f-list-item-wrap'):
                houseUrl = prefix + item.find(class_='dd-item title').a['href']
                title = item.find(class_='dd-item title').a['title']
                try:
                    locations = item.select('.area')[0].find_all('a')
                    location = locations[0].string + ' ' + locations[2].string
                except:
                    location = None
                if location:
                    csv_writer.writerow([title, location, houseUrl])
            if not url:
                break
        else:
            break


def crawl_fangtx():
    url = 'http://zu.sh.fang.com/house/i3{page}/'
    prefix = 'http://zu.sh.fang.com'
    csv_file = open('fangtx.csv', 'w')
    csv_writer = csv.writer(csv_file, delimiter=',')
    print('start fetch fangtx..')
    for i in tqdm(range(1, 101)):
        sleep(1)
        response = requests.get(url.format(page=i), headers=header, allow_redirects=False)
        if response.status_code == 200:
            html = BeautifulSoup(response.text, 'lxml')
            for item in html.select('.list .info'):
                try:
                    houseUrl = prefix + item.select('.title')[0].a['href']
                    title = item.select('.title')[0].a['title']
                    locations = item.find_all(class_='gray6 mt20')[0].find_all('a')
                    location = locations[0].string + ' ' + locations[1].string + ' ' + locations[2].string
                    csv_writer.writerow([title, houseUrl, location])
                except:
                    pass
        else:
            break


if __name__ == '__main__':
    try:
        crawl_lianjia()
        print('fetch lianjia done!')
    except:
        print('链家网挂了，需要更新抓取规则～')
    '''
    在Python中，每个模块都有一个名称，如果它被直接运行，那么它的名称就是__main__。如果它被导入到其他模块中，那么它的名称就是它的文件名（不包括.py扩展名）。

try块中的代码会尝试调用crawl_lianjia()函数，然后打印一条消息表示抓取链家网的操作已经完成。如果在执行try块中的代码时发生了任何异常，那么就会执行except块中的代码，打印一条消息表示链家网挂了，需要更新抓取规则。
    '''

    try:
        crawl_anjuke()
        print('fetch anjuke done!')
    except:
        print('安居客挂了，需要更新抓取规则～')

    try:
        crawl_58()
        print('fetch 58 done!')

    except:
        print('58同城挂了，需要更新抓取规则～')

    try:
        crawl_ganji()
        print('fetch ganji done!')
    except:
        print('赶集网挂了，需要更新抓取规则～')

    try:
        crawl_fangtx()
        print('fetch fangtx done!')
    except:
        print('房天下挂了，需要更新抓取规则～')
