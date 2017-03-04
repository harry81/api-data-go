# -*- coding: utf-8 -*-
import re
import requests
import csv
from lxml import etree

url = 'https://www.data.go.kr/search/index.do'
# ALL, DATA, OPENAPI, DATAGRID
params = {
    "index": "ALL",
    # "query": u"상가",
    "currentPage": 1,
    "countPerPage": 100,
}


def list_of_api(url=url):
    response = requests.get(url, params=params)
    tree = etree.HTML(response.content)
    resp = []

    for ele in tree.xpath("//div[contains(@class, 'data-item')]"):
        api = {}
        category = ele.xpath("span[contains(@class, 'visible-desktop')]/text()")[0]
        api["category"] = category.strip()

        title = ele.xpath("div[contains(@class, 'data-title')]/a/text()")[0]
        api["title"] = title.strip()

        read = ele.xpath("div[contains(@class, 'data-title')]/span/text()")[0]
        read = re.search('([0-9])+', read).group()
        api["read"] = read.strip()

        download = ele.xpath("div[contains(@class, 'data-title')]/span/text()")[1]
        try:
            download = re.search('([0-9])+', download).group()
            api["download"] = download.strip()
        except Exception as e:
            print e
            api["download"] = '0'

        desc = ele.xpath("div[contains(@class, 'data-desc')]/text()")[0]
        api["desc"] = desc.strip()

        resp.append(api)

    return resp


def main():
    apis = list_of_api(url)
    cnt = 0

    with open('open-api.csv', 'wb') as csvfile:
        for api in apis:
            apiwriter = csv.writer(csvfile, delimiter=',', quotechar='|')
            apiwriter.writerow([api[k].encode('utf8') for k in api])
            # print "%4d [%s %s] %s - %s" % (
            #     cnt, api['read'], api['download'], api['title'], api['desc'])
            cnt += 1


if __name__ == '__main__':
    main()
