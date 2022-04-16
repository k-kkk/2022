# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:19:49 2021

@author: ASUS
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Radar

plt.rcParams['font.sans-serif'] = 'SimHei' #设置字体

job_info_new = pd.read_csv(r'C:\Users\ASUS\job_info_new.csv',encoding='GBK')

job_info_new["工资水平"] = pd.to_numeric(job_info_new["工资水平"],errors='coerce')
job_info_new.head()
    
### 1、热门岗位可视化
import random
a = job_info_new['岗位名'].value_counts()[:10]

plt.subplots_adjust(bottom=0.01)
plt.xticks(rotation=45)
plt.title('招聘岗位排行榜前10名')
colors = ['#FF0000', '#0000CD', '#00BFFF', '#008000', '#FF1493', '#FFD700', '#FF4500', '#00FA9A', '#191970', '#9932CC']
random.shuffle(colors)
plt.bar(a.index,a,color = colors)
plt.rcParams['savefig.dpi'] = 300 #图片像素
plt.rcParams['figure.dpi'] = 300 #分辨率

plt.show()

#2、热门招聘公司可视化
a = job_info_new['公司名'].value_counts()[:10]
plt.figure(figsize=(16,9))
plt.rcParams['font.sans-serif'] = 'SimHei' #设置字体
plt.subplots_adjust(bottom=0.25)
plt.xticks(rotation=45)
plt.title('招聘公司排行榜前10名')
plt.bar(a.index,a)
plt.show()

### 1、热门岗位可视化

b = job_info_new['岗位名'].value_counts()[:10]
c = (
    Bar()
    .add_xaxis(list(b.index))
    .add_yaxis("招聘行业数量", [270, 115, 111, 68, 57, 55, 51, 50, 50, 37]) #list(a.values)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=15)),
        title_opts=opts.TitleOpts(title="招聘行业排行榜前10名"),
    )
    .render('1.html')
)
c

#2、热门招聘公司可视化

a = job_info_new['公司名'].value_counts()[:10]
c = (
    Bar()
    .add_xaxis(list(a.index))
    .add_yaxis("招聘岗位数量", [80, 63, 45, 38, 37, 35, 34, 34, 29, 28]) #list(a.values)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=15)),
        title_opts=opts.TitleOpts(title="招聘公司排行榜前10名"),
    )
    .render('2.html')
)
c

#3、招聘岗位数最多的10个城市

data = job_info_new[job_info_new['工作城市'] != '异地招聘']['工作城市'].value_counts()[:10]#有些是异地招聘过滤掉

c = (
    Bar()
    .add_xaxis(list(data.index))
    .add_yaxis("招聘岗位数量", [1138,  967,  680,  660,  446,  364,  343,  315,  220,  150]) 
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
        title_opts=opts.TitleOpts(title="招聘岗位数最多的10个城市"),
    )
    .render('3.html')
)
c

#4、算法工程师在各个城市的需求量
data = job_info_new[job_info_new['岗位名'] == '算法工程师']
data_1 = data[data['工作城市'] != '异地招聘']['工作城市'].value_counts()[:10]

index = list(data_1.index)
values = [56, 27, 22, 17, 17, 13, 13, 11, 10, 8]


c = (
    Pie()
    .add(
        "",
         [list(z) for z in zip(index,values)],
        center=["55%", "50%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="算法工程师在各个城市的需求量"),
        legend_opts=opts.LegendOpts(pos_left="40%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    .render('9.html')
)
c

##4、一线城市公司规模雷达

v1 = []
for city in ['北京', '上海', '广州', '深圳']:
    v = []
    a = ['少于50人', '50-150人', '150-500人', '500-1000人', '1000-5000人', '5000-10000人', '10000人以上']
    dic = {}
    df1 = job_info_new[job_info_new['工作城市'] == '{}'.format(city)].groupby(by='公司规模').count()
    index = list(df1.index)
    value = [int(i[0]) for i in df1.values.tolist()]
    for t in zip(index, value):
        dic[t[0]] = t[1]
   # print(dic)
    for i in a:  # 这个for循环的作用是按a列表的顺序在字典进行取值，画图可以看出层次感
        if i in dic:
            v.append(dic[i])
    v1.append(v)
#print(v1)


v2 = [v1[0]]
v3 = [v1[1]]
v4 = [v1[2]]
v5 = [v1[3]]
c = (
    Radar()
    .add_schema(
        schema=[
            opts.RadarIndicatorItem(name='少于50人', max_=200),
            opts.RadarIndicatorItem(name='50-150人', max_=400),
            opts.RadarIndicatorItem(name='150-500人', max_=300),
            opts.RadarIndicatorItem(name='500-1000人', max_=170),
            opts.RadarIndicatorItem(name='5000-10000人', max_=180),
            opts.RadarIndicatorItem(name='10000人以上', max_=150),
        ]
    )
    .add("北京", v2)
    .add("上海", v3)
    .add("广州", v4)
    .add("深圳", v5)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    .set_global_opts(
        legend_opts=opts.LegendOpts(selected_mode="single"),
        title_opts=opts.TitleOpts(title="一线城市公司规模"),
    )
    .render('4.html')
)
c

##5、主要招聘类别
index = list(job_info_new.groupby(by='类别').count().sort_values('序号', ascending=False).index)
values = list(job_info_new.groupby(by='类别').count()['序号'].values)


c = (
    Pie()
    .add(
        "",
         [list(z) for z in zip(index,values)],
        center=["55%", "50%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="招聘类别"),
        legend_opts=opts.LegendOpts(pos_left="25%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render('5.html')
)
c

#6、工资分布
index =  list(job_info_new.groupby(by='工资').count()['序号'].sort_values(ascending=False).index)[:6]
values = list(job_info_new.groupby(by='工资').count()['序号'].sort_values(ascending=False).values)[:6]
c = (
    Pie()
    .add(
        "",
        [list(z) for z in zip(index,values)],
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="工资分布"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("6.html")
)
c


#7、工作经验与薪资关系图
attr = []  # 这个列表在后面会作为后面画图的x轴标签
v1 = []    # 这个列表在后面会作为后面画图的y轴标签
df4 = job_info_new.groupby(by='工作经验')['工资水平'].mean() 
index = list(df4.index)  
value = df4.values.tolist()
dic = {}  # 用于存储index和value的对应元素作为键值对
for i in zip(index, value):
    dic[i[0]] = i[1]
d_order = sorted(dic.items(), key=lambda x: x[1], reverse=False)  # 使用sorted方法对字典的值进行排序，返回的结果是一个列表，包含多个二元列表
for i in d_order:  # 使用for循环遍历d_order列表，取出对应值
    attr.append(i[0])
    v1.append(i[1])
    v1 = [int(x) for x in v1]

from pyecharts.charts import Bar

from pyecharts.globals import ThemeType

bar = (
    Bar()
    .add_xaxis(list(attr))
    .add_yaxis("工资水平", v1)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=15)),
        title_opts=opts.TitleOpts(title="工作经验与薪资关系图"),
    )
)
line = (Line().add_xaxis(list(attr)).add_yaxis("工资水平", v1))
bar.overlap(line)
bar.render('7.html')



#8、学历与薪资关系图
attr = []  # 这个列表在后面会作为后面画图的x轴标签
v1 = []    # 这个列表在后面会作为后面画图的y轴标签
df4 = job_info_new.groupby(by='学历')['工资水平'].mean() 
index = list(df4.index)  
value = df4.values.tolist()
dic = {}  # 用于存储index和value的对应元素作为键值对
for i in zip(index, value):
    dic[i[0]] = i[1]
d_order = sorted(dic.items(), key=lambda x: x[1], reverse=False)  # 使用sorted方法对字典的值进行排序，返回的结果是一个列表，包含多个二元列表
for i in d_order:  # 使用for循环遍历d_order列表，取出对应值
    attr.append(i[0])
    v1.append(i[1])
    v1 = [int(x) for x in v1]

bar = (
    Bar()
    .add_xaxis(list(attr))
    .add_yaxis("工资水平", v1)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
        title_opts=opts.TitleOpts(title="学历与薪资关系图"),
    )
)

line = (Line().add_xaxis(list(attr)).add_yaxis("工资水平", v1))
bar.overlap(line)
bar.render('8.html')


#9、工作简介词云图
def get_word_cloud(data=None):
    words = []
    describe = data['工作简介'].str[1:-1]
    describe.dropna(inplace=True)
    [words.extend(i.split(',')) for i in describe]
    words = pd.Series(words)
    word_fre = words.value_counts()
    word_fre = word_fre[1:,]
    return word_fre

word_fre = get_word_cloud(data=job_info_new) #可看看开发工程师，算法
wordcloud = WordCloud(background_color='white',
                       width=500,
                       height=500,
                       margin=2,
                       max_words=500,  # 设置最多显示的词数
                       font_path="simhei.ttf",  # 中文词图必须设置字体格式，否则会乱码，这里加载的是黑体
                       random_state=10)  # 设置有多少种随机生成状态，即有多少种配色方案
w = wordcloud.fit_words(dict(word_fre))  # 传入需画词云图的文本
plt.imshow(w)
plt.axis('off')  # 关闭坐标轴
plt.show()
w.to_file('1.png')  # 图片保存





