# !/usr/bin/python
# -*- coding=utf8 -*-
import urllib2

def test():
	url = 'http://adapp.10jokes.com'
	req=urllib2.Request(url) 
	req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)") 
	file = urllib2.urlopen(req)
	content = file.read()
	print content

if __name__ == '__main__':
	for i in range(1,1000):
		test()