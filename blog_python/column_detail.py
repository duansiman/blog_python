#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-04 09:59:41
# Project: test

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.base_url='http://blog.csdn.net/column/details/mysqlcentury.html?&page='
        self.page_num=1
        self.total_num=2

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num <= self.total_num:
            url = self.base_url + str(self.page_num)
            print(url)
            self.crawl(url, callback=self.index_page)
            self.page_num += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for aList in response.doc('ul.detail_list a[href^="http"]').items():
            print(aList.attr.href)
            self.crawl(aList.attr.href, callback=self.detail_page)
        for lis in response.doc('ul.detail_list p.detail_p').items():
            print(lis.text())
        for ems in response.doc('ul.detail_list em').items():
            print(ems.text())

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
