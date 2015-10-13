# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取所给网页所有图片

from BeautifulSoup import *
import urllib2
import sys
from facepp import API

API_KEY = 'e650f1c9f43900a5316906c658caa8be'
API_SECRET = 'ron72ejcgEA6vR6BfIFD-UBBA8pFQ_QL'

# 打印所有图片地址
def print_img_src(img_srcs):
	for src in img_srcs:
		print src

# 判断一张图片中是否有人脸
def face_filter(img_src):
	p_result = None
	api = API(API_KEY, API_SECRET)
	for i in range(0,5):
		try:
			p_result = api.detection.detect(url = img_src)['face']
			break
		except:
			continue
	if p_result != None and len(p_result) == 1:
		return True
	else:
		return False
	

# 爬取所给网站所有图片
def crawl_images(page_link):
	img_list = []
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=10)
	soup = BeautifulSoup(f.read())
	img_tags = soup.findAll('img')
	img_srcs = map(lambda x:x['src'],img_tags)
	for src in img_srcs:
		if face_filter(src) == True:
			img_list.append(src)
	return img_list

def main(page_link):
	img_srcs = crawl_images(page_link)
	print_img_src(img_srcs)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		page_link = sys.argv[1]
		main(page_link)
	

