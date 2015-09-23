# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 抓取明星脸数据
from BeautifulSoup import BeautifulSoup
import urllib2
import DB
import json

separator = None

# 连接数据库 
def Connent_Online_Mysql_By_DB(hostname,port,username,pwd,dbname,socket):
    db = DB.DB(False,host=hostname, port=port, user=username ,passwd=pwd, db=dbname,charset='gbk', unix_socket=socket) 
    return db

# 写入数据库
def write_record_db(db,list_obj,table_name):
    try:
        db.insert(table_name,list_obj)
        db.commit()
    except Exception,e:
        print e	

def crawl_face_data():
	g_link = 'http://ent.qq.com/c/oumei_star.shtml'
	r = urllib2.Request(g_link)
	f = urllib2.urlopen(r, data=None, timeout=10)
	soup = BeautifulSoup(f.read())
	star_lines = soup.find('div',{'class':'index_cot_list'}).find('dd').findAll('td')
	for star_line in star_lines:
		if star_line.find('a') != None:
			star_link = star_line.find('a')['href']
			print star_link

def analyse_data(db,star_data,face_link):
	global separator
	all_tags = star_data.findAll('td')
	if separator == None:
		separator = all_tags[1].text[3:][3]
	username = all_tags[1].text[3:].split(separator)
	if len(username) > 1:
		username = username[0] + ' ' + username[1]
	else:
		username = username[0]
	print username
	# username = all_tags[1].text[3:].encode('utf-8').decode('utf-8')
	sex = all_tags[4].text[3:].encode('utf-8').decode('utf-8')
	enname = all_tags[5].text[4:].encode('utf-8').decode('utf-8')
	birth = (all_tags[6].text[4:] + all_tags[7].text[3:]).encode('utf-8').decode('utf-8')
	xingzuo = all_tags[8].text[3:].encode('utf-8').decode('utf-8')
	guoji = all_tags[9].text[3:].encode('utf-8').decode('utf-8')
	district = all_tags[10].text[3:].encode('utf-8').decode('utf-8')
	profession = all_tags[11].text[3:].encode('utf-8').decode('utf-8')
	height = all_tags[12].text[3:].encode('utf-8').decode('utf-8')
	blood = all_tags[13].text[3:].encode('utf-8').decode('utf-8')
	# print face_link
	record = {}
	record['face_img_link'] = face_link
	record['star_district'] = district
	record['birth_date'] = birth
	record['cert_name'] = username
	record['en_name'] = enname
	record['constellatory'] = xingzuo
	record['profession'] = profession
	record['height'] = height
	record['blood_type'] = blood
	record['star_country'] = guoji
	record['sex'] = sex
	write_record_db(db,record,'faceapp_star_user')
	# for tag in all_tags:
	
def push_data_into_db(db):
	f = open('all_star.link','r')
	rc = f.readlines()
	rc = map(lambda x: x.strip(), rc)
	for line in rc:
		try:
			r = urllib2.Request(line)
			f = urllib2.urlopen(r, data=None, timeout=10)
			soup = BeautifulSoup(f.read())
		except:
			continue
		star_data = soup.find('table',{'width':'300'})
		face_link = soup.find('div',{'id':'star_face'}).find('a').find('img')['src']
		analyse_data(db,star_data,face_link)

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','faceapp','/tmp/mysql.sock')
	push_data_into_db(db)
	# crawl_face_data() 