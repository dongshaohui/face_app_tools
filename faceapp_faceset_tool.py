# -*- coding: utf-8 -*-
# author : Dong Shaohui
# description : 检查mysql数据库中，url中是否有人脸，并归类至group

import DB
import urllib
from facepp import API
import json
import sys,os

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

# faceset进行训练
def train_faceset(db,faceset_type):
	faceset_id = db.select("select face_plus_id from faceapp_face_set where face_set_type = '" + faceset_type + "'")[0][0]
	params = urllib.urlencode({'api_key': API_KEY,'api_secret':API_SECRET,'faceset_id':faceset_id})
	train_faceset_url = 'https://apicn.faceplusplus.com/v2/train/search?%s' % params
	f = urllib.urlopen(train_faceset_url)
	result = json.loads(f.read())
	print result
	session_id = result['session_id']
	print session_id

# 检查session信息
def check_session(session_id):
	params = urllib.urlencode({'api_key': API_KEY,'api_secret':API_SECRET,'session_id':session_id})
	session_url = 'https://apicn.faceplusplus.com/v2/info/get_session?%s'  % params
	f = urllib.urlopen(session_url)
	print f.read()

# 查看faceset信息
def check_faceset_info(db,faceset_type):
	faceset_id = db.select("select face_plus_id from faceapp_face_set where face_set_type = '" + faceset_type + "'")[0][0]
	params = urllib.urlencode({'api_key': API_KEY,'api_secret':API_SECRET,'faceset_id':faceset_id})
	check_faceset_url = 'https://apicn.faceplusplus.com/v2/faceset/get_info?%s' % params
	f = urllib.urlopen(check_faceset_url)
	result = json.loads(f.read())
	faces = result['face']
	print (str)(len(faces)) + ' 张人脸'
	
	face_id_list = map(lambda x:x['face_id'],faces)

	# 查看是否有faceid-users表中是否有faceid缺失
	face_id_user_list = db.select("select face_id from faceapp_star_faceid_user")
	face_id_user_list = map(lambda x:x[0],face_id_user_list)
	
	# 查看差集
	face_id_diff_list = (set)(face_id_list) - (set)(face_id_user_list)
	print face_id_diff_list

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','faceapp','/tmp/mysql.sock')
	if sys.argv[1] == 'check_face_set':
		check_faceset_info(db,sys.argv[2])
	elif sys.argv[1] == 'add_face_into_face_set':
		print 'add face'
	elif sys.argv[1] == 'train_faceset':
		train_faceset(db,sys.argv[2])
	elif sys.argv[1] == 'check_session':
		check_session(sys.argv[2])