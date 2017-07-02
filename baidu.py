from urllib import request

with request.urlopen('http://www.baidu.com') as f:
	data = f.read()
	print('status:',f.status, f.reason)
	print('data:', data.decode('utf-8'))