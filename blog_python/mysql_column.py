from urllib import request
import re
import logging

# <div class="column_list ">
#   <div style="background-image:url(http://img.blog.csdn.net/20151123174942067)" class="column_bg"></div>

#   <a href="/column/details/postgresql.html" class="column_list_link" target="_blank">
#         <div class="column_c">
#           <p class="column_list_p">PostgreSQL系列</p>
#           <div class="column_list_b">
#             <div class="column_list_b_l fl"><i class="fa fa-file-text-o"></i><span>16</span></div>
#             <div class="column_list_b_r fr"><i class="fa fa-eye"></i><span>193766</span></div>
#           </div>
#         </div>
#    </a>
# </div>

try:
	with request.urlopen('http://blog.csdn.net/database/column.html?&page=1', ) as f:
		content = f.read().decode('utf-8')
	print('status:',f.status, f.reason)
	pattern = re.compile('<div.*?column_list ">.*?'
	+ '<a.*?"(.*?)".*?'
	+ '<p.*?column_list_p">(.*?)</p>.*?'
	+ '<div.*?column_list_b_l.*?<span>(.*?)</span>.*?'
	+ '<div.*?column_list_b_r.*?<span>(.*?)</span>'
	, re.S)

	items = re.findall(pattern, content)
	print(items)
	for item in items:
		print("url->", item[0], "title->", item[1], "fileCount->", item[2], "fileEye->", item[3])
except Exception as e:
	print('take place exception')
	logging.exception(e)
finally:
	pass





