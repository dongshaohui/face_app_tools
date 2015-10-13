# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取所有明星数据

import DB
import urllib
from facepp import API
import json
import sys,os,urllib2
from BeautifulSoup import *

API_KEY = 'e650f1c9f43900a5316906c658caa8be'
API_SECRET = 'ron72ejcgEA6vR6BfIFD-UBBA8pFQ_QL'

# 连接数据库
def Connent_Online_Mysql_By_DB(hostname,port,username,pwd,dbname,socket):
    db = DB.DB(False,host=hostname, port=port, user=username ,passwd=pwd, db=dbname,charset='gbk', unix_socket=socket) 
    return db

# 更新数据库
def update_record_db(db,list_obj,cond_obj,table_name):
	try:
		db.update(table_name,list_obj,cond_obj)
		db.commit()
	except Exception,e:
		print e

# 写入数据库
def write_record_db(db,list_obj,table_name):
    try:
        db.insert(table_name,list_obj)
        db.commit()
    except Exception,e:
        print e

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

def clean_str(info):
	index = info.find('：')
	return info[index+3:]


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

# 爬取明星图片
def crawl_star_imgs(img_page_link):
	star_imgs = []
	root_link = img_page_link[:img_page_link.rfind('/')+1]
	r = None
	f = None
	# 获取页数
	try:
		r = urllib2.Request(img_page_link)
		f = urllib2.urlopen(r, data=None, timeout=10)	
	except:
		return []
	soup = BeautifulSoup(f.read())
	page_num = None
	if str.isdigit(soup.find('div',{'id':'page'}).findAll('a')[-2].text.encode('utf-8')) == True:
		page_num = (int)(soup.find('div',{'id':'page'}).findAll('a')[-2].text.encode('utf-8'))
	else:
		page_num = (int)(soup.find('div',{'id':'page'}).findAll('a')[-3].text.encode('utf-8'))
	for i in range(1,page_num+1):
		link = root_link + (str)(i) + '.html'
		try:
			r2 = urllib2.Request(link)
			f2 = urllib2.urlopen(r2, data=None, timeout=10)	
			soup2 = BeautifulSoup(f2.read())
			star_img_link = soup2.find('div',{'class':'img_box'}).find('img')['src']
			if face_filter(star_img_link) == True:
				star_imgs.append(star_img_link)
		except:
			print link,' error!'
			continue
	return star_imgs

# 解析明星详情
def parse_star_info(info_link):
	info_tags = ['出生','星座','身高','体重','职业']
	info_tags_index = []
	r = urllib2.Request(info_link)
	f = urllib2.urlopen(r, data=None, timeout=10)	
	soup = BeautifulSoup(f.read())
	info_header = soup.find('div',{'class':'wrapper1220 cm_block01'})
	
	# 解析明星信息
	star_summary = info_header.find('h3',{'class':'txt01'}).text[:-2] # 明星简介
	star_info = info_header.find('div',{'class':'txt02'}).text.encode('utf-8')
	for tag in info_tags:
		info_tags_index.append(star_info.find(tag))
	
	location = clean_str(star_info[info_tags_index[0]:info_tags_index[1]])
	constellation = clean_str(star_info[info_tags_index[1]:info_tags_index[2]])
	height = clean_str(star_info[info_tags_index[2]:info_tags_index[3]]) + ' CM'
	weight = clean_str(star_info[info_tags_index[3]:info_tags_index[4]]) + ' KG'
	profession = clean_str(star_info[info_tags_index[4]:])
	star_imgs = []
	# 爬取明星写真
	star_img_urls = soup.find('ul',{'id':'xiezhen'}).findAll('li')
	for img_url_obj in star_img_urls:
		img_url = img_url_obj.find('a')['href']
		star_imgs += crawl_star_imgs(img_url)
	
	return location,constellation,height,weight,profession,star_imgs
	
	
def crawl_star_info(db,page_link):
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=10)
	soup = BeautifulSoup(f.read())	
	boxes = soup.findAll('div',{'class':'ulbox'})
	for box in boxes:
		lis = box.findAll('li')
		for li in lis:
			name = li.text
			front_img_link = li.find('img')['src']
			info_link = li.find('a')['href']
			location,constellation,height,weight,profession,star_imgs = parse_star_info(info_link)
			print name,star_imgs
			# print location

def crawl_all_star_info(db):
	page_links = ['http://www.mingxing.com/ziliao/index.html','http://www.mingxing.com/ziliao/index_2.html',
				'http://www.mingxing.com/ziliao/index_3.html','http://www.mingxing.com/ziliao/index_4.html',
				'http://www.mingxing.com/ziliao/index_5.html','http://www.mingxing.com/ziliao/index_6.html']
	for page_link in page_links:
		crawl_star_info(db,page_link)

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','faceapp','/tmp/mysql.sock')
	crawl_all_star_info(db)