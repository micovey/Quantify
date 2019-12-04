# -*- coding: utf-8 -*-
import baostock as bs
import pandas as pd
import numpy as np
import datetime

#### 登陆系统 ####

lg = bs.login()
########定义变量#######
now_time=datetime.datetime.now().strftime('%Y-%m-%d')
now_time=datetime.datetime.strptime(now_time,'%Y-%m-%d')
year=int(now_time.year)
print('请输入地址')
global file_place
file_place='D:\\'
fl = 'Quantify\\idcode.csv'
filee=file_place+fl
fff=file_place+'\\Quantify\\daily\\daily'+str(2019)+'.csv'
# D:\\Quantify\\idcode.csv
idcode = pd.read_csv(filee,header=None)
if len(idcode) > 10:
    print('读取成功')
else:
    print('读取失败')
idcode = np.array(idcode)
global datalength
datalength=180

#######定义函数########
##滚动删除数据
def drop_date_row(drop_data):
    drop_data['date'] = [datetime.datetime.strptime(str(x), '%Y/%m/%d') for x in drop_data['date']]
    now_time=datetime.datetime.now().strftime('%Y-%m-%d')
    now_time=datetime.datetime.strptime(now_time,'%Y-%m-%d')
    min_date = drop_data['date'].min()
    drop_date = now_time + datetime.timedelta(days=-datalength)
    if min_date <drop_date:
        drop_data = drop_data.drop(drop_data[drop_data.date < drop_date].index)
        return(drop_data)
    else:
        drop_data=pd.DataFrame()
        return(drop_data )
##滚动获得数据
def get_daily_data(id,start_date_find,end_date_find):
    rs = bs.query_history_k_data_plus(id,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST,peTTM,pbMRQ,psTTM,pcfNcfTTM",
        start_date=str(start_date_find), end_date=str(end_date_find),
        frequency="d", adjustflag="3")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields,index=range(0,len(data_list)))
    result["turn"] = [0 if x == "" else float(x) for x in result["turn"]]
    result["volume"] = [0 if x == "" else float(x) for x in result["volume"]]
    result["close"] = [0 if x == "" else float(x) for x in result["close"]]
    marketvalue=result["volume"] / result["turn"]*result["close"]*100
  #  marketvalue=result.apply(lambda x: x["volume"] / x["turn"]*x["close"]*100, axis=1)
    result["marketvalue"]=marketvalue
 #   print( result)
    return(result)
##开始，结束下载日期
def check_download(check_date):
    if len(check_date)==0:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d')
        start_date = now_time + datetime.timedelta(days=-datalength)
        start_date = str(datetime.datetime.strftime(start_date, '%Y-%m-%d'))
    else:
        start_date = check_date['date'].max()
        start_date += datetime.timedelta(days=+1)
        start_date = str(datetime.datetime.strftime(start_date, '%Y-%m-%d'))
    end_date=str(datetime.datetime.now().strftime('%Y-%m-%d'))
    return start_date,end_date


##删除重复项
def drop_duplicates(drop_data):
    n1=len(drop_data)
    drop_data['date'] = [datetime.datetime.strptime(x, '%Y/%m/%d') for x in drop_data['date']]
    drop_data.drop_duplicates(subset=['code','date'],keep='first',inplace=True)
    n2=len(drop_data)
    if n1==n2:
        drop_data = pd.DataFrame()
        return (drop_data)
    else:
        return (drop_data)


#####开始计算###########
######滚动删除数据
drop_data = pd.read_csv(fff)
print(len(drop_data))
if len(drop_data)>0:
    drop_data = drop_date_row(drop_data)
    if len(drop_data)<2:
        print("不需要删除数据")
    else:
        print("已删除数据")
        drop_data = drop_data.dropna(axis=0, how='all')
        drop_data['date'] = [datetime.datetime.strftime(x, '%Y/%m/%d') for x in drop_data['date']]
        drop_data.to_csv(fff, header=True, index=False)
else:
    print("没有数据")

##查看是否需要更新数据
check_date = pd.read_csv(fff)

check_date['date']=[datetime.datetime.strptime(x,'%Y/%m/%d') for x in check_date['date']]
start_date,end_date=check_download(check_date)
##历史行情数据下载
if datetime.datetime.strptime(start_date,'%Y-%m-%d')<=datetime.datetime.strptime(end_date,'%Y-%m-%d'):
    if datetime.datetime.strptime(end_date,'%Y-%m-%d')==datetime.datetime.strptime(start_date,'%Y-%m-%d') and int(datetime.datetime.now().hour)<18:
        print("不需要更新数据，当日没有结束")
    else:
        for id in idcode:
            id=str(id)
            id=id[2:11]#提取9位代码
            print('=====' + id + '=====')
            result1=get_daily_data(id,start_date,end_date)
            result1["date"] = [np.nan if x == "" else x for x in result1["date"]]
            result1 = result1.dropna(axis=0, how='any')
            if len(result1) > 0:
                result1['date'] = [datetime.datetime.strptime(x,'%Y-%m-%d') for x in result1['date']]
                result1['quarter']=[int((x.month-1)/3)+1 for x in result1['date']]
                result1['year']=[int(x.year) for x in result1['date']]
                result1['date'] = [datetime.datetime.strftime(x, '%Y/%m/%d') for x in result1['date']]
                result1.to_csv(fff, mode='a', header=False)
            else:
                continue
else:
    print("不需要更新数据，没有开始新交易")
bs.logout()


##删除重复项
drop_data = pd.read_csv(fff)
drop_data = drop_duplicates(drop_data)
if len(drop_data)<2:
    print("没有重复项")
else:
    print("已删除重复项")
    drop_data['date'] = [datetime.datetime.strftime(x, '%Y/%m/%d') for x in drop_data['date']]
    drop_data.to_csv(fff, header=True, index=False)



daily_data = pd.read_csv(fff)
def cal_rets(x):
    x['ret'] = (np.log(x['close'])-np.log(x['close']).shift(1))[1:]*100
    return x

returndata=daily_data.groupby('code').apply(cal_rets)
returndata= pd.DataFrame(returndata)
returndata = returndata.dropna(axis=0, how='any')
returndata.to_csv(fff, header=True,index=False)