# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:29:31 2021

@author: ASUS
"""
import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

job_info_new = pd.read_csv('job_info_new.csv',encoding='GBK')
pandas_profiling.ProfileReport(job_info_new).to_file("report1.html")