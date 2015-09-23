# !/usr/bin/python
# -*- coding=utf8 -*-
# author : Shaohui Dong
# description : 爬取恒富宝数据(恒富天下)
from BeautifulSoup import BeautifulSoup
import sys,os,urllib2,threading
import datetime
import json
import re
import DB

g_root_link = "https://www.hengfu100.com/productHFBList"
g_pro_link = "https://www.hengfu100.com/"

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

def fetch_web_data(db):
	page_link = g_root_link
	r = urllib2.Request(page_link)
	f = urllib2.urlopen(r, data=None, timeout=10)
	soup = BeautifulSoup(f.read())
	prolist = soup.find('div',{'class':'layout fix H-container'}).findAll('div',{'class':'fix product-Li hengfb-Li'})
	for product in prolist:
		if product.find('div',{'class':'p-time'}).find('a')['class'] != 'btn1':
			break
		# 爬取正在进行中的恒富宝理财产品
		record = {}
		record['proName'] = product.find('a')['title']
		record['amount'] = product.find('ul').findAll('li')[2].find('b').text.replace(',','')
		record['surplus'] = product.find('b',{'class':'fw-B'}).text.replace(',','')
		record['interest'] = product.find('ul').findAll('li')[0].find('span').text
		# record['add_interest'] = product.find('div',{'class':'list_product_right'}).find('table').findAll('td')[1].text.replace('+','')
		record['progress'] = product.find('ul',{'class':'fl pro-mid'}).find('li').text
		record['progress'] = re.findall(r"\d+\.?\d*",record['progress'])[0]
		record['duetime'] = product.find('ul').findAll('li')[1].find('span').text
		# record['endtime'] = product.find('ul',{'class':'ul_2'}).find('li',{'class':'li_menu'}).find('a')['endtime']
		record['datestr'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		record['urllink'] = g_pro_link + product.find('a')['href']
		write_record_db(db,record,'p2p_product_hengfu_hengfubao')

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','financal_product','/tmp/mysql.sock')
	# 清空原有数据库
	script_path = os.getcwd()
	script_path = script_path[:script_path.find('p2p3000')]+"p2p3000/tool/empty_db_table.sh"
	os.system(script_path + '  p2p_product_hengfu_hengfubao')
	# os.system('/home/dong/p2p3000/tool/empty_db_table.sh  p2p_product_hengfu_hengfubao')
	fetch_web_data(db)

