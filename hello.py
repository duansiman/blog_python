#!/usr/bin/env python3
from collections import Iterable
import os


print("-------------------Dict------------------")
dict = {'a':1,'b':2,'c':3}
for key in dict:
	print(key)
print('\n')

for v in dict.values():
	print(v)	
print('\n')

for k, v in dict.items():
	print("key:",k,"value:", v)
print('\n')

print("-------------------Iterable------------------")
print(isinstance("abc", Iterable))
print('\n')

for i, value in enumerate(['a','b','c']):
	print(i, value)
print('\n')

list2 = list(range(1,11))
for value in list2:
	print(value)
print("\n")

list3 = [x * x for x in range(1, 11)];
for value in list3:
	print(value)
print("\n")

list4 = [m + n for m in 'ABC' for n in 'XYZ'];
for value in list4:
	print(value)
print("\n")

print("-------------------OS file------------------")
files = [d for d in os.listdir('.')]
for file in files:
	print(file)
print('\n')

L = ['Hello', 'World', 'IBM', 'Apple']
for v in [s.lower() for s in L]:
	print(v)
print('\n')

print("-------------------generator------------------")
g = (x * x for x in range(10))
for x in g:
	print(x)
print('\n')

n, a, b = 0, 0, 1
print('n',n,'a',a,'b',b)

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'
fib = fib(2)
print(next(fib))
print(next(fib))

# age = input()

# age = int(age)
age = 10
if age>30:
	print('old person')
else:
	print('yonger person')

sum = 0
for x in range(10):
	sum = sum + x
print(sum)

dect = {'devin':21}
print(dect['devin'])

def my_abc(x):
	if not isinstance(x, (int, float)):
		raise 	TypeError('bad type')
	if x > 0:
		return x
	else:
		return -x

result = my_abc(-5)
print(result)