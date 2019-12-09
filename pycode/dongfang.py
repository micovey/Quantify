#coding=utf-8
import requests
import re
import pandas as pd
def get_Data(begin,end):
	headers = {
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
	}
	url ='http://push2his.eastmoney.com/api/qt/stock/kline/get?secid=1.000001&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57&klt=5&fqt=0&beg={}&end={}&ut=fa5fd1943c7b386f172d6893dbfba10b&cb=cb74924124192872'.format(begin,end)
	r = requests.get(url,headers=headers)
	html = r.text
	reg1 = re.compile(r'"klines":(.*?);')
	data = reg1.findall(html)
	data = data[0]
	data = data[2:-5]
	return data



def sort(data):
	list_data=data.split('\",\"')##第一次切分，一条分钟数据
	day=[]
	open1=[]
	high=[]
	low=[]
	close=[]
	vol=[]
	amount=[]
	for l in list_data:
		daily=l[0:-1]
		item=daily.split(',')##第二次切分，开盘、收盘等
		day.append(item[0])
		open1.append(float(item[1]))
		high.append(float(item[2]))
		low.append(float(item[3]))
		close.append(float(item[4]))
		vol.append(float(item[5]))
		amount.append(float(item[6]))
		df=pd.DataFrame({"date":day,"open":open1,"high":high,"low":low,"close":close,"vol":vol,"amount":amount})
	return df

data=get_Data("20191101","20200101")
df = sort(data)
print(df)