#!/usr/bin/python3

import os
import re
import math
from random import randint
import uuid
import datetime

"""os.system("echo 'hello world'")"""

def generate_long_num(legth):
	result = ''
	while legth > 0:
		legth = legth-1
		number = randint(0, 9)
		result = result + str(number)

	return result


def generate_email(name):
	fname, surname = name[0], name[1]
	result = fname[0:3] + "_" + surname[0:3] + "@gmail.com"
	return result

def generate_created():
	result = ''
	year = str(randint(1990, 2015))
	result = result + year
	month = zero_num(12)
	result = result + '.' + month
	if month != '02':
		day = zero_num(30)
	else:
		day = zero_num(28)
	result = result + '.' + day + " "
	hour = zero_num(23)
	result = result + hour
	minute = zero_num(59)
	result = result + ':' + str(minute)
	second = zero_num(59)
	result = result + ':' + str(second)

	return result

def get_resources(rel_file_path):
	result = []
	path_name = os.path.dirname(__file__) + rel_file_path
	with open(path_name, encoding='utf-8') as names_file:
 		for name in names_file:
 			result.append(name)

 		return result

def generate_uuid():
 	return uuid.uuid4()
	

def zero_num(max):
	result = randint(0, max)
	if result < 10:
		result = '0' + str(result)
	return str(result)

def wrap_one_line_json(key, value, is_not_last = True):
	comma = ""
	if is_not_last:
		comma = ", "
	return '    "' + key + '": "' + value + '"' + comma

names = get_resources('/res/names.txt')
surnames = get_resources('/res/surnames.txt')
cities = get_resources('/res/cities.txt')

def get_jsons(counter_big):
	
	fullnames = []

	i = 0
	while i<1000:
		lenname = len(names) - 1
		len_surname = len(surnames) - 1
	# print(lenname)
	# fullname = names[randint(0, lenname)] + ' ' + surnames[randint(0, len_surname)]
		fullname = (names[randint(0, lenname)].replace('\n', ''), surnames[randint(0, len_surname)].replace('\n', ''))
	# fullname = fullname.replace('\n', '')
	# print(fullname)
		fullnames.append(fullname)
		i += 1

# senders = set(fullnames)
# senders = []
# print(len(senders))



# if math.fmod(len(senders), 2) != 0:
# 	i = len(senders) -1
# 	senders.pop()

# receivers = set()
# i = len(senders)/2
# while i>0:
# 	i = i - 1
# 	receivers.add(senders.pop())


	pairs = set()

	while (len(fullnames) != 0):
		json_str = ""
		counter_big -=1
		curl = "curl -XPOST 'http://localhost:9200/test_elastic/users/" + str(counter_big) + "' -d    \'{ "
		json_str += curl
		name_tuple = fullnames.pop()
		name = name_tuple[0]
		surname = name_tuple[1]
		name_str = wrap_one_line_json('firstname', name)
		surname_str = wrap_one_line_json('surname', surname)
		json_str += wrap_one_line_json('id', str(generate_uuid()))
		json_str += name_str
		json_str += surname_str
		city_raw = cities[randint(0, len(cities) - 1)]
		city_raw = city_raw.replace("\n", '')
		city = wrap_one_line_json('location', city_raw)
	# print(city)
		json_str +=city
		email = wrap_one_line_json('email', generate_email(name_tuple))
	# print(email)
		json_str += email
		phone = generate_long_num(10)
		json_str +=wrap_one_line_json('phone', phone)
		json_str +=wrap_one_line_json('is_deleted', 'false')
		registered = generate_created()
		json_str +=wrap_one_line_json('registered', registered, False)
		json_str += '}\' \n'
		pairs.add(json_str)
	


# 	inserts = os.path.dirname(__file__) + "/result.txt"
# # print(os.getcwd())
# 	counter = 1
# 	if os.path.isfile(inserts):
# 		while os.path.isfile(inserts):
# 			inserts = os.path.dirname(__file__) + "/result" + str(counter) + ".txt"
# 			counter += 1

# 	result_file = open(inserts, 'w+', encoding = 'utf-8')
# 	for pair in pairs:
# 		result_file.write(pair)
	return pairs

counter = 5000000
while counter>=0:
	print("\n    Left to make: " + str(counter) + "\n")
	# print("\n    Time: " + str(counter) + "\n")
	begin_time = datetime.datetime.now()
	pairs = get_jsons(counter)
	counter -= 1000
	while len(pairs)>0:
		pair = pairs.pop()
		# print(pair)
		os.system(pair)
		if len(pairs) == 1:
			end_time = datetime.datetime.now()
			delta = (end_time-begin_time).total_seconds()
			print("\n \n " + str(delta) + "\n \n ")
	
	# os.system("echo '" + pair)

