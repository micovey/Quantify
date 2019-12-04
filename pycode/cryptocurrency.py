#coding=utf-8
import requests
import re
import pandas as pd
import numpy as np
NAME=["Bitcoin","binance-coin","bitcoin-cash","bitcoin-sv","Cardano","Cosmos","Dash","EOS","ethereum","ethereum-classic"]#,"IOTA","Litecoin","Monero","NEO","ontology","Stellar","Tezos","TRON","vechain","XRP"]
def get_data(name):
    url = 'https://coinmarketcap.com/currencies/'+name+'/historical-data/?start=20190803&end=20191203'
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'}
    response = requests.get(url,headers = headers) 
    response.encoding = response.apparent_encoding
    html = response.text##获取文本
    print(html)
    reg1 = re.compile(r'"quotes"([\s\S]*?),"related":')
    data = reg1.findall(html)##匹配到交易信息部分
    data=data[0]##匹配到交易信息部分
    reg2 = re.compile(r'"time_open":"([\s\S]*?)T00:00:00.000Z')    
    day= reg2.findall(data)##提取日期
    reg3 = re.compile(r'"close":([\s\S]*?),"volume"')    
    close= reg3.findall(data)##提取价格
    close=np.array(close, dtype='float32')
    return day,close

df_all=pd.DataFrame(columns=["day","asset","close","return"])

for name in NAME:
	day,close=get_data(name)
	day=day[1:]
	ret =np.diff(np.log(close), n=1,axis=-1)*100
	close=close[1:]
	df=pd.DataFrame({"day":day,"asset":name,"close":close,"return":ret})
	df_all=df_all.append(df)
	print(name)
df_all.to_csv("D:\\Quantify\\daily\\cryptocurrency", header=True,index=False)##输出