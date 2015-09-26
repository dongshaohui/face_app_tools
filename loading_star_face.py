# -*- coding: utf-8 -*-
# author : Dong Shaohui
# description : 检查mysql数据库中，url中是否有人脸，并归类至group

import DB
from PIL import Image,ImageDraw
import urllib
from facepp import API
import json
import socket

API_KEY = 'e650f1c9f43900a5316906c658caa8be'
API_SECRET = 'ron72ejcgEA6vR6BfIFD-UBBA8pFQ_QL'

def Connent_Online_Mysql_By_DB(hostname,port,username,pwd,dbname,socket):
    db = DB.DB(False,host=hostname, port=port, user=username ,passwd=pwd, db=dbname,charset='gbk', unix_socket=socket) 
    return db

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

# 男性
# def loading_star_male_face(db):
# 	star_face_result = db.select('select face_img_link from faceapp_star_user where is_valid = 1 and sex = "M"')
# 	# 建立get请求
# 	params = urllib.urlencode({'api_key': API_KEY,'api_secret':API_SECRET})
# 	male_faceset_id = '5b7716066b070a7649f3ddf3c5b4f46d'
# 	api = API(API_KEY, API_SECRET)
# 	for result in star_face_result:
# 		p_image = result[0]
# 		p_result = None
# 		try:
# 			p_result = api.detection.detect(url = p_image)['face']
# 			face_id = p_result[0]['face_id']
# 			add_face_params = urllib.urlencode({'api_key': API_KEY,'api_secret':API_SECRET,'faceset_id':male_faceset_id,'face_id':face_id})
# 			add_face_url = 'https://apicn.faceplusplus.com/v2/faceset/add_face?' + add_face_params
# 			f = urllib.urlopen(add_face_url)
# 			print f.read()
# 		except:
# 			print p_id,'error'
# 			continue

def loading_faceset(db,star_face_result,faceset_id):
	# 建立get请求
	params = urllib.urlencode({'api_key': API_KEY,'api_secret':API_SECRET})
	api = API(API_KEY, API_SECRET)
	for result in star_face_result:
		p_image = result[0]
		p_id = result[1]
		p_result = None
		try:
			p_result = api.detection.detect(url = p_image)['face']
			face_id = p_result[0]['face_id']
			add_face_params = urllib.urlencode({'api_key': API_KEY,'api_secret':API_SECRET,'faceset_id':faceset_id,'face_id':face_id})
			add_face_url = 'https://apicn.faceplusplus.com/v2/faceset/add_face?' + add_face_params
			f = urllib.urlopen(add_face_url)
			
			add_result = json.loads(f.read())
			if 'added' in add_result:
				if (int)(add_result['added']) == 1:
					print face_id,' face added!'
					record = {}
					record['face_id'] = face_id
					record['star_user_id'] = p_id
					write_record_db(db,record,'faceapp_star_faceid_user')
					
		except:
			print face_id,'error'
			continue		
	

def pre_run(db):
	male_star_face_result = db.select('select face_img_link,id from faceapp_star_user where is_valid = 1 and sex = "M"')
	female_star_face_result = db.select('select face_img_link,id from faceapp_star_user where is_valid = 1 and sex = "F"')
	loading_faceset(db,male_star_face_result,'dceed1f5a2b90814c26d10bd254a6f4c')

def check_image_valid(db):
	api = API(API_KEY, API_SECRET)
	all_result = db.select('select id,face_img_link from faceapp_star_user where is_valid = 1')
	for result in all_result:
		p_id = result[0]
		p_image = result[1]
		p_result = None
		try:
			p_result = api.detection.detect(url = p_image)['face']
		except:
			print p_id,'error'
			continue
		print p_id
		if len(p_result) != 1:
			# change tag invalid
			record = {}
			cond = {}
			record['is_valid'] = 0
			cond['id'] = p_id
			update_record_db(db,record,cond,'faceapp_star_user')
			

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','faceapp','/tmp/mysql.sock')
	pre_run(db)
	