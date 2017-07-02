__author__ = 'epdc'
# -*- coding:utf-8 -*-

from urllib import request
import re
import logging

CSDN_COLUMN_DOMAIN='http://blog.csdn.net/'

class CsdnColumn:
	def __init__(self):
		self.columns = []

	def getColumnPage(self, category, pageIndex):
		try:
			with request.urlopen(CSDN_COLUMN_DOMAIN + category + '/column.html?&page=' + str(pageIndex)) as f:
				content = f.read().decode('utf-8')
			return content;
		except Exception as e:
			logging.exception(e)
			print('take place exception :', "category : ", category, " pageIndex : ", pageIndex)
			return None

	def parseColumnPage(self, category, pageIndex):
		content = self.getColumnPage(category, pageIndex)
		if not content:
			return None
		pattern = re.compile('<div.*?column_list ">.*?'
			+ '<a.*?"(.*?)".*?'
			+ '<p.*?column_list_p">(.*?)</p>.*?'
			+ '<div.*?column_list_b_l.*?<span>(.*?)</span>.*?'
			+ '<div.*?column_list_b_r.*?<span>(.*?)</span>'
			, re.S)

		items = re.findall(pattern, content)
		columns = []
		for item in items:
			dict = {}
			dict['column_url'] = item[0]
			dict['column_title'] = item[1]
			dict['column_article_count'] = item[2]
			dict['column_read_count'] = item[3]
			columns.append(dict)
		return columns

	def startColumn(self):
		category = 'database'
		for pageIndex in range(16):
			columns = self.parseColumnPage(category, pageIndex+1)
			if not columns:
				print("category:", category, "pageIndex:", pageIndex, "failured")
			print("category:", category, "pageIndex:", pageIndex, "succeed", "columns size", len(columns))
			for column in columns:
				self.columns.append(column)

		print(category, "column size:", len(self.columns))
		for column in self.columns:
			print("url:", column.get('column_url'), "title:", column.get('column_title'), "articleCount:", column.get('column_article_count'), "readCount:", column.get('column_read_count'))

csdnColumn = CsdnColumn()
csdnColumn.startColumn()