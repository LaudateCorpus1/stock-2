#coding: utf-8

from selenium import webdriver

import time
import os
import re

import urllib2
import sys
from bs4 import BeautifulSoup

import os
import logging
import time
from datetime import datetime
from datetime import timedelta
from datetime import date


import threading  
import time 
import json
 

def start(url, d):
   # try:
    browser = webdriver.Chrome(executable_path='F:\chromedriver_win32\chromedriver.exe')
    url = url
    browser.get(url)
    try:
	    t = browser.page_source

	    pn = re.compile(ur'(.*)"statuses":(.*?)}]', re.S)
	    match = pn.match(t)
	    if not match:
	        browser.close()
	        browser.quit()
	    	return 0
	    result =  match.group(2)
	    result = result + '}]'
	    decode = json.loads(result)
	    
	    f = open('stock.txt', 'r')


	    today   = date.today()
	    print today
	    startDetect = time.time()
	    ed = int(time.mktime(datetime.strptime(datetime.strftime(today, "%Y-%m-%d"), "%Y-%m-%d").timetuple()))
	    st = int(time.mktime(datetime.strptime(datetime.strftime(today - timedelta(days = 1), "%Y-%m-%d"), "%Y-%m-%d").timetuple()))
	    st = str(st) + '000'
	    print st
	    ed = str(ed) + '000'
	    print ed

	    while 1:
			line = f.readline()

			if not line:
				break
			#print line
			array = line[:-1].split('%')
			for item in decode:
				print item['created_at'], st, ed
				if str(item['created_at']) > st and str(item['created_at']) < ed:
					if item['description'].encode('utf-8').find(array[1]) != -1:
					#	print 2
						print array[1], item['description'].encode('utf-8')
						if d.has_key(array[1]):
							d[array[1]] = d[array[1]] + 1
						else:
							d[array[1]] = 1
				elif str(item['created_at']) < st:
					#print 1
					browser.close()
					browser.quit()
					return 0

			#print array[0], array[1]
			


	   # print decode[0]['description'].encode('utf-8')

	    browser.close()
	    browser.quit()
    except:
    	print 'error'
		browser.close()
		browser.quit()	

def get_id():

	url = 'http://xueqiu.com/people/all'
	
	headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
	req = urllib2.Request( url, headers = headers)
	try:
		content = urllib2.urlopen(req).read()
	except:
		return
	soup = BeautifulSoup(content)
	
	name = soup.find('ul',class_='tab_nav')
	h = name.findAll('a')
	f = open('id.txt', 'w')
	people = {}
	for item in h:
		link = item.get('href')
		if link.find('id') != -1:

			url = 'http://xueqiu.com' + link
			print url
			headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
			req = urllib2.Request( url, headers = headers)
			try:
				content = urllib2.urlopen(req).read()
			except:
				return
			soup = BeautifulSoup(content)
			name = soup.find('ul',class_='people')
			h = name.findAll('li')
			for item in h:
				p = item.findAll('input')
				print p[0].get('value').encode('utf-8'), p[1].get('value').encode('utf-8')
				if not people.has_key(p[0].get('value').encode('utf-8')):
					people[p[0].get('value').encode('utf-8')] = 0
					f.write(p[0].get('value').encode('utf-8') + ' ' + p[1].get('value').encode('utf-8') + '\n')


def pawner():

	f = open('id.txt', 'r')
	yesterday = datetime.strftime(date.today() - timedelta(days = 1), "%Y-%m-%d")
	score_file = 'score' + yesterday + '.txt'
	#ff = open('score' + yesterday + '.txt', 'r')
	d = {}
	#while 1:
	#	score = ff.readline()
	#	if not score:
	#		break
	#	array = score[:-1].split(' ')
	#	d[array[0]] = int(array[1])
	#ff.close()
	#i = 1000000000
	while 1:
		try:
			line = f.readline()
		#	user = str(i)
			if not line:
				break
			array = line[:-1].split(' ')
			user = array[0]
			print array[0], array[1]
			#user = "1676206424"
			page = 1
			while 1:

				url = "http://xueqiu.com/" + user + "?page=" + str(page)
				ret = start(url, d)
				if ret == 0:
					#print i
					break
				page = page + 1
			time.sleep(5)
		except:
			continue
		#break
		#i = i  + 1
		#if i >=9999999999:
		#	break
	f.close()
	ff = open(score_file, 'w')
	t = sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	for key in t:
		#print str(key[0]) + ' ' + str(key[1]) + '\n'
		ff.write(str(key[0]) + ' ' + str(key[1]) + '\n')

    #id = 'backwasabi'
    #url = "http://xueqiu.com/" + id
    #start(url)


#	timer = threading.Timer(7200, pawner)
#	timer.start()

if __name__ == "__main__":



##	timer = threading.Timer(7200, pawner)
#	timer.start()

	#get_id()
	pawner()