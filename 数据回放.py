# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:26:03 2021

@author: ASUS
"""
import pandas as pd

job_info_new = pd.read_csv('job_info_new.csv',encoding='GBK')

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://root:3283655@localhost/mysql')
#engine = create_engine('dialect+driver://username:password@host:port/database')
#dialect -- 数据库类型,driver -- 数据库驱动选择,username -- 数据库用户名,password -- 用户密码
#host 服务器地址,port 端口,database 数据库
job_info_new.to_sql('job_info_new',engine,schema='mysql',if_exists='replace',index=False,index_label=False)