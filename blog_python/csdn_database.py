#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-05 14:40:40
# Project: mysql

from pyspider.libs.base_handler import *
from mysqldb import DBManager
import re


class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.base_url='http://blog.csdn.net/database/column.html?&page='
        self.page_num=1
        self.total_num=16
        self.dbManager = DBManager()

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num <= self.total_num:
            url = self.base_url + str(self.page_num)
            self.crawl(url, callback=self.index_page)
            self.page_num += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        urls = []
        for aTag in response.doc('div.column_list a[href^="http"]').items():
            urls.append(aTag.attr.href) 
        titles = []
        for pTag in response.doc('div.column_list p.column_list_p').items():
            titles.append(pTag.text())
        readCounts = [] 
        for spanTag in response.doc('div.column_list div.column_list_b_r span').items():
            readCounts.append(spanTag.text())
        
        result = []
        for i, title in enumerate(titles):
            if title.lower().find('mysql')>=0:
                columns = {}
                columns['url']=urls[i]
                columns['title']=titles[i]
                columns['readCount']=readCounts[i]
                result.append(columns)
                
            
        for column in result:
            print(column.get('url'))
            print(column.get('title'))
            print(column.get('readCount'))
            sql = 'insert into t_csdn_columns(url,title,read_count) values(%(url)s, %(title)s, %(readCount)s)'
            self.dbManager.execute(sql, column)
            print('\n')
        for column in result:
            self.crawl(column.get('url'), callback=self.column_detail)

    @config(age=10 * 24 * 60 * 60)
    def column_detail(self, response):
        detail_total_page=1;
        for spanTag in response.doc('div.page_nav span').items():
            pattern = re.compile('共(.*?)页')
            items = re.findall(pattern, spanTag.text())
            detail_total_page = int(items[0])
        detail_cur_page = 1
        while detail_cur_page <= detail_total_page:
            url = response.url + '?&page=' + str(detail_cur_page)
            self.crawl(url, callback=self.column_detail_page)
            detail_cur_page += 1
        #[200] len:20981 -> result:None fol:0 msg:0 err:UnboundLocalError("local variable 'detail_total_page' referenced before assignment",)
            
    @config(age=10 * 24 * 60 * 60)
    def column_detail_page(self, response):
        urls = []
        titles = []
        for aTag in response.doc('ul.detail_list a[href^="http"]').items():
            urls.append(aTag.attr.href) 
            titles.append(aTag.text())
            
        descs = []
        for pTag in response.doc('ul.detail_list p.detail_p').items():
            descs.append(pTag.text())
            
        readCounts = [] 
        for emTag in response.doc('ul.detail_list div.detail_b em').items():
            readCounts.append(emTag.text())
            
        result = []
        for i, title in enumerate(titles):
            articleDesc = {}
            articleDesc['url']=urls[i]
            articleDesc['title']=titles[i]
            articleDesc['desc']=descs[i]
            articleDesc['readCount']=readCounts[i]
            result.append(articleDesc)
            
        for articleDesc in result:
            self.crawl(articleDesc.get('url'), callback=self.detail_page, save={'articleDesc': articleDesc})            
            
            
    @config(priority=2)
    def detail_page(self, response):
        articleDesc = response.save['articleDesc']
        for aTag in response.doc('div#panel_Profile a.user_name').items():
            articleDesc['userName'] = aTag.text()
            articleDesc['authorLink'] = aTag.attr.href
        
        for spanTag in response.doc('div.article_r span.link_comments').items():
            pattern = re.compile('\((.*?)\)')
            items = re.findall(pattern, spanTag.text())
            articleDesc['commentCount'] = int(items[0])
        for spanTag in response.doc('div.article_r span.link_postdate').items():
            articleDesc['date'] = spanTag.text()
        
        for ddTag in response.doc('dl#btnDigg dd').items():
            articleDesc['likeCount'] = int(ddTag.text())
        
        for divTag in response.doc('div#article_content').items():
            articleDesc['articleContent'] = divTag.html()
        
        for aTag in response.doc('div.article_l span.link_categories a').items():
            articleDesc['labelList'] = articleDesc.get('labelList', '') + aTag.text() + ','
        
        sql = 'insert into t_csdn_article(type,url,title,`desc`,read_count,article_content,date,author,comment_count,label_list,like_count,author_link) values(1, %(url)s, %(title)s, %(desc)s, %(readCount)s, %(articleContent)s, %(date)s, %(userName)s, %(commentCount)s, %(labelList)s, %(likeCount)s, %(authorLink)s)'
        self.dbManager.execute(sql, articleDesc)
        return articleDesc
