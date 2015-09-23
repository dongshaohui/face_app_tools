#!/usr/local/python/bin
# coding=utf-8
import DB
import json
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

def trans(db):
	features = db.select('select * from faceapp_facial_feature')
	for feature in features:
		f_type_title = feature[1]
		all_types = json.loads(feature[2])
		for key in all_types:
			for f_type_key in all_types[key]:
				record = {}
				f_type = all_types[key][f_type_key] 
				cn_type = f_type['type']
				cn_desc = f_type['desc']
				en_type = f_type_key
				record['feature_type_desc'] = cn_desc
				record['feature_type_title_en'] = en_type
				record['feature_type_title_cn'] = cn_type
				record['facial_type'] = f_type_title
				# print f_type_title
				write_record_db(db,record,'faceapp_face_feature_type')

		

if __name__ == '__main__':
	db = Connent_Online_Mysql_By_DB('rdsjjuvbqjjuvbqout.mysql.rds.aliyuncs.com',3306,'dongsh','5561225','faceapp','/tmp/mysql.sock')
	trans(db)