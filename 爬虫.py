# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:02:18 2021

@author: ASUS
"""
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
import pandas as pd
import time,random
import json


#url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
url_qian = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD,2,'
url_hou = '.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

for j in range(1,2): #250页
    url = url_qian+str(j)+url_hou
    response = requests.get(url, headers=headers) # 发送网络请求
    if response.status_code != 200:
        print('第',j,'页爬取失败，进入下一页爬虫！')
        continue
    response.encoding = 'GBK'  # 设置中文方式编码
    #print('文本源码', response.text)
    #print('状态码', response.status_code)
    
    bs = BeautifulSoup(response.text,'html.parser')

    #bs = bs.find_all('script',{'type':'text/javascript'})[2]
    #info = re.findall('{"type":"engine_search_result",(.*?),"adid":""}',str(bs))
    
    info = re.compile('window.__SEARCH_RESULT__ =(.+)</script>').findall(response.text)
        
    job_name = []  # 记录岗位名
    company_name = []  # 记录公司名  
    workarea_text = []  # 记录工作地点
    salary = []  #记录工资
    issuedate = []  # 记录发布时间
    company_type = []  # 记录公司类型
    company_size = []  # 记录公司人数
    company_ind = []  # 记录行业
    job_msg = []  # 工作描述

    education = []#学历
    work_experience = []#工作经验
    limit_people = []#招聘人数
    
    for i in range(50):
        #infoi=eval("{"+info[i]+"}")
        
        infoi= json.loads(''.join(info))
        infoi = infoi['engine_search_result'][i]
        
        job_name.append(re.sub(r'\\','',infoi['job_name']))
        company_name.append(infoi['company_name'])
        workarea_text.append(infoi['workarea_text'])
        
        salary.append(re.sub(r'\\','',infoi['providesalary_text']))
        issuedate.append(infoi['issuedate'])
        company_type.append(infoi['companytype_text'])
        company_size.append(infoi['companysize_text'])
        #company_ind.append(infoi['companyind_text'])
        company_ind.append(re.sub(r'\\','',infoi['companyind_text']))

        
        education.append("".join([i for i in infoi['attribute_text'] if i in '本科大专应届生在校生硕士博士']))# 通过列表推导式获取学历
        work_experience.append("".join([i for i in infoi['attribute_text'] if '经验' in i ]))
        limit_people.append("".join([i for i in infoi['attribute_text'] if '招' in i]))
        
        url_sub=infoi['job_href']
        url_sub=re.sub('////','',re.sub(r'\\','//',url_sub))
        response_sub=requests.get(url_sub,headers=headers)
        response_sub.encoding = 'GBK'
        dom = etree.HTML(response_sub.text)
        job_msg.append(dom.xpath('//div[@class="tCompany_main"]//div[@class="bmsg job_msg inbox"]/p/text()'))   
        #time.sleep(random.uniform(0,0.5))
        
    da = pd.DataFrame()
 
    da['岗位名'] = job_name
    da['公司名'] = company_name
    da['工作地点'] = workarea_text
    da['工资'] = salary
    da['学历'] = education
    da['工作经验'] = work_experience
    da['招聘人数'] = limit_people
    da['发布时间'] = issuedate
    da['公司类型'] = company_type
    da['公司人数'] = company_size
    da['行业'] = company_ind
    da['工作描述'] = job_msg 
    
    
    try:
        da.to_csv('job_info_org1.csv', encoding='GBK', header=None)
        print('第',j,'页爬取完毕！')
        #print(da)
        #time.sleep(random.uniform(0,0.5))
    except:
        print('第',j,'页爬取失败，进入下一页爬虫！')