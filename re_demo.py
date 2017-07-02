import re

pattern = re.compile(r'world')
match = re.search(pattern, 'hello wold')
print(match)
if match:
	print(match.group())