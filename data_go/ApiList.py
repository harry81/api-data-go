# -*- coding: utf-8 -*-
import re
import requests
import csv
from lxml import etree


def list_of_api(query=None, countPerPage=100):
    url = 'https://www.data.go.kr/search/index.do'

    # ALL, DATA, OPENAPI, DATAGRID
    params = {
        "index": "DATA",
        "query": query,
        "currentPage": 1,
        "countPerPage": countPerPage,
    }

    response = requests.get(url, params=params)
    tree = etree.HTML(response.content)
    resp = []

    for ele in tree.xpath("//div[contains(@class, 'data-item')]"):
        api = {}
        category = ele.xpath("span[contains(@class, 'visible-desktop')]/text()")[0]
        api["category"] = category.strip().encode('utf-8')

        title = ele.xpath("div[contains(@class, 'data-title')]/a/text()")[0]
        api["title"] = title.strip().encode('utf-8')

        read = ele.xpath("div[contains(@class, 'data-title')]/span/text()")[0]
        read = re.search('([0-9])+', read).group()
        api["read"] = read.strip().encode('utf-8')

        download = ele.xpath("div[contains(@class, 'data-title')]/span/text()")[1]
        try:
            download = re.search('([0-9])+', download).group()
            api["download"] = download.strip().encode('utf-8')
        except Exception as e:
            api["download"] = '0'

        desc = ele.xpath("div[contains(@class, 'data-desc')]/text()")[0]
        api["desc"] = desc.strip().encode('utf-8')

        resp.append(api)

    return resp


def main():
    apis = list_of_api(countPerPage=30)
    cnt = 0

    with open('open-api.csv', 'wb') as csvfile:
        # apiwriter = csv.writer(csvfile, delimiter=',', quotechar='\"')
        fieldnames = ['category', 'read', 'download', 'title', 'desc']
        apiwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        apiwriter.writeheader()
        for api in apis:
            # apiwriter.writerow([api[k].encode('utf8') for k in api])
            apiwriter.writerow(api)
            cnt += 1


if __name__ == '__main__':
    main()
