# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:03:44 2021

@author: ASUS
"""
import pandas as pd
import numpy as np
import re
import jieba
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
plt.rcParams['font.sans-serif'] = ['SimHei']

data = pd.read_csv(r'C:\Users\ASUS\job_info_org.csv',encoding='GBK',header=None, index_col=0)

#1、为数据添加列名
data.index = range(1,len(data)+1)
data.columns = ['岗位名','公司名','工作地点','工资','学历','工作经验','招聘人数','发布日期','公司类型','公司规模','行业','工作描述']
data.shape#(12507, 12)

data.drop_duplicates(subset=['岗位名','公司名','学历','工作地点'],keep='first',inplace=True)#去重操作
data.shape#(10609, 12)

#2、缺失值统计
data.isnull().sum()

cols = data.columns
colours = ['#000099', '#ffff00']
fig = sns.heatmap(data[cols].isnull(), cmap=sns.color_palette(colours))
heatmap = fig.get_figure()
heatmap.savefig('2.png', dpi = 300)

msno.bar(data[cols],figsize=(30,8),color='r',fontsize=20,labels=True)

#缺失数据的百分比列表
for col in data.columns:
    pct_missing = np.mean(data[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100)))
    
#3、岗位名称信息探索
data['岗位名'].str.strip().astype(str).apply(lambda x: x.lower())  #去掉前后空格、转字符串类型、转小写
data['岗位名'].value_counts()

#4、用规范名称替换岗位名称
job_list = ['数据分析', '数据挖掘', '算法', '大数据',
            '工程师', '运营', '软件工程', '前端开发',
            '深度学习', 'AI', '数据库', '数据库', '数据产品',
            '客服', 'java', '.net', 'andrio', '人工智能', 'c++',
            '数据管理','图像识别','经理','Python工程师','机器学习','推荐系统','云计算','开发','物联网','自然语言处理','架构师','软件']
job_list = np.array(job_list) #为方便通过索引引用
def rename(x=None, name_list=job_list):
    index = [i in x for i in job_list]
    if sum(index)>0:
        return job_list[index][0]
    else:
        x

data['类别'] = data['岗位名'].apply(rename)
data['类别'].value_counts()

data.dropna(subset=['类别'],inplace=True)
data.shape #(7314, 13)

#5、工作地点分割为工作城市
# 按 - 分割   expand=True  0那一列重新赋值给df['city']
data['工作城市'] = data['工作地点'].str.split('-', expand=True)[0]
data.head(5)

#6、工资区间管理
def get_max_min(x=None):
    try:
        if x[-3] == '万':
            a = [float(i)*10000 for i in re.findall('\d+\.?\d*', x)]
        elif x[-3] == '千':
            a = [float(i)*1000 for i in re.findall('\d+\.?\d*', x)]
        if x[-1] == '年':
            a = [i/12 for i in a]
        return a
    except:
        return x
    
salary = data['工资'].apply(get_max_min)
data['最低工资'] = salary.str[0]
data['最高工资'] = salary.str[1]
data['工资水平'] = data[['最低工资','最高工资']].apply('mean')
#最低最高工资异常值处理
data["最低工资"] = pd.to_numeric(data["最低工资"],errors='coerce')
data["最高工资"] = pd.to_numeric(data["最高工资"],errors='coerce')
sns.set_context("poster")
plt.figure(figsize=(10,10))
sns.boxplot(y="最低工资",data=data);#最低工资离群值

sns.set_context("poster")
plt.figure(figsize=(10,10))
sns.boxplot(y="最高工资",data=data); #最高工资离群值

#为了准确性，把月薪大于15K的离群点
data = data[data.最低工资 <100000]
data = data[data.最高工资 <100000]

#7、工作描述处理
data['工作描述'].value_counts()

with open(r'C:\Users\ASUS\stopwords.txt', 'r',encoding = 'utf-8') as f: #停用词处理
    stopword = f.read()
a = data['工作描述'].str[2:-2].apply(lambda x: x.lower()).apply(lambda x: ''.join(x)).apply(jieba.lcut).apply(lambda x: [i for i in x if i not in stopword])
a[a.apply(lambda x: len(x) < 6)] = np.nan  
data['工作简介'] = a

#8、数据清洗后的数据，保存为job_info_new.csv
data['序号'] = [i+1 for i in range(len(data))]
data.columns
features = ['序号','岗位名','类别', '公司名', '工作地点', '工作城市','最低工资', '最高工资','工资','工资水平', '学历','工作经验', '招聘人数','公司类型','公司规模', '行业', '工作简介','工作描述','发布日期']
data_new = data[features]
data_new.to_csv('job_info_new.csv', encoding='GBK', index=None)


