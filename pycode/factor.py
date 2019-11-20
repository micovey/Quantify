# -*- coding: utf-8 -*-
import baostock as bs
import pandas as pd
import numpy as np
import datetime
###下载因子所需数据
#### 登陆系统 ####
lg = bs.login()
########定义变量#######
now_time=datetime.datetime.now().strftime('%Y-%m-%d')
now_time=datetime.datetime.strptime(now_time,'%Y-%m-%d')
year=int(now_time.year)-1##需要两年，6月前后算两次。
start_date1=str(int(year)+1)+'-06-28'##六月末按照市值分组，需要根据计算年份更改日期
start_date2=str(int(year)+1)+'-12-31'##12月末，需要根据计算年份更改日期
end_date1=start_date1##提取一天的数据
end_date2=start_date2##提取一天的数据

print('请输入地址')
global file_place
file_place='D:\\'##自行更改
fl = 'Quantify\\idcode.csv'
filee=file_place+fl
fff=file_place+'\\Quantify\\factor\\factor'+str(year+1)+'.csv'
print('请输入地址')

fl = 'Quantify\\idcode.csv'
filee=file_place+fl
# D:\\Quantify\\idcode.csv
idcode = pd.read_csv(filee,header=None)##公司代码，为了循环
if len(idcode) > 10:
    print('读取成功')
else:
    print('读取失败')
idcode = np.array(idcode)
quar=4##年报数据，第四季度
##账面价值
def get_profit_data(id,year,quar):
    profit_list = []
    rs_profit = bs.query_profit_data(code=id, year=year, quarter=quar)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    result_profit["liqaShare"] = [1 if x == "" else float(x) for x in result_profit["liqaShare"]]
    return(result_profit)
##流通市值
def get_history_data(id,start_date,end_date):
    rs = bs.query_history_k_data_plus(id,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
                                      start_date=start_date, end_date=end_date,
                                      frequency="d", adjustflag="3")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result["turn"] = [0 if x == "" else float(x) for x in result["turn"]]
    result["volume"] = [0 if x == "" else float(x) for x in result["volume"]]
    result["close"] = [0 if x == "" else float(x) for x in result["close"]]
    marketvalue=result["volume"] / result["turn"]*result["close"]*100
    result["marketvalue"] = marketvalue
    return(result)



##历史行情数据下载
for id in idcode:
    id=str(id)
    id=id[2:11]##提取9位代码
    print('=====' + id + '=====')
    result1=get_profit_data(id,year,quar)##账面价值
    result2=get_history_data(id,start_date2,end_date2)##12月末账面价值比
    result_1= pd.merge(result1, result2, on=['code'])
    result_1["book_market"]=result_1["marketvalue"]/result_1["liqaShare"]
    result11 = result_1[['code','book_market']]
    result3 = get_history_data(id, start_date1, end_date1)##6月末流通市值
    result_2 = pd.merge(result11, result3, on=['code'])
    result= result_2[['code','book_market','marketvalue']]
    if len(result1) > 0:
        result.loc[0, 3] = int(year) + 1##为此后方便计算
        result.to_csv(fff, mode='a', header=None)
    else:
        continue

##退出登录
bs.logout()