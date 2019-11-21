import pandas as pd
import baostock as bs
import datetime
import math

now_time=datetime.datetime.now().strftime('%Y-%m-%d')
now_time=datetime.datetime.strptime(now_time,'%Y-%m-%d')
year=int(now_time.year)
print('请输入地址')
global file_place
file_place='D:\\'
fl = 'Quantify\\idcode.csv'
filee=file_place+fl
fff=file_place+'\\Quantify\\daily\\daily'+str(2019)+'.csv'



returndata = pd.read_csv(file_place+'Quantify\\daily\\daily_ret'+str(2019)+'.csv')
factor_data2019=pd.read_csv(file_place+'Quantify\\factor\\factor_sort'+str(2019)+'.csv')
factor_data2019["year"] =2019
factor_data2018=pd.read_csv(file_place+'Quantify\\factor\\factor_sort'+str(2018)+'.csv')
factor_data2018["year"] =2018
returndata ["year"] = [2018 if x <3  else 2019 for x in returndata ["quarter"]]
half_1= pd.merge(returndata, factor_data2018, on=['code','year'])
half_2= pd.merge(returndata, factor_data2019, on=['code','year'])
half_1=half_1.append(half_2)
factor3=half_1[["date","code","ret","smb_dum","hml_dum","marketvalue"]]
small=[]
day=[]
big=[]
##计算因子
for group in factor3.groupby(['date','smb_dum']):
    group=group[1]
    group["sum_m"] = group['marketvalue'].sum()
    group["ret_w"] = group['marketvalue']/group['sum_m']*group['ret']
    group["ret_group"]=group['ret_w'].sum()
    group=group[["date","smb_dum","ret_group"]]
    if group.iloc[0,1]==1:
        small.append(group.iloc[0,2])
        day.append(group.iloc[0,0])
    else:
        big.append(group.iloc[0,2])

df_smb=pd.DataFrame({'date':day,'small':small,'big':big})
df_smb["smb"]=df_smb["small"]-df_smb["big"]
df_smb=df_smb[["date","smb"]]
#print(df_smb)
#df_smb.to_csv(file_place+'Quantify\\daily\\smb'+str(2019)+'.csv', header=True,index=False)

high=[]
low=[]
day=[]
for group in factor3.groupby(['date','hml_dum']):
    group=group[1]
    group["sum_m"] = group['marketvalue'].sum()
    group["ret_w"] = group['marketvalue']/group['sum_m']*group['ret']
    group["ret_group"]=group['ret_w'].sum()
    group=group[["date","hml_dum","ret_group"]]
    if group.iloc[0,1]==2:
        low.append(group.iloc[0,2])
        day.append(group.iloc[0,0])
    elif group.iloc[0,1]==0:
        high.append(group.iloc[0,2])
    else:
        continue

df_hml=pd.DataFrame({'date':day,'high':high,'low':low})
df_hml["hml"]=df_hml["high"]-df_hml["low"]
df_hml=df_hml[["date","hml"]]

#print(df_hml)
#df_hml.to_csv(file_place+'Quantify\\daily\\hml'+str(2019)+'.csv', header=True,index=False)

returndata['date']=[datetime.datetime.strptime(x,'%Y/%m/%d') for x in returndata['date']]
start_date = df_hml['date'].min()
start_date = datetime.datetime.strptime(start_date, '%Y/%m/%d')
start_date = start_date + datetime.timedelta(days=-1)
start_date = str(datetime.datetime.strftime(start_date, '%Y-%m-%d'))
end_date=str(datetime.datetime.now().strftime('%Y-%m-%d'))

##寻找大盘指数
#### 登陆系统 ####

lg = bs.login()

rs = bs.query_history_k_data_plus("sh.000001",
    "date,code,open,high,low,close,preclose,volume,amount,pctChg",
    start_date=start_date, end_date=end_date, frequency="d")
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
ret_m = pd.DataFrame(data_list, columns=rs.fields)
ret_m=ret_m[["date","close"]]
ret_m['close_down1'] = ret_m['close'].shift(periods=1)
ret_m = ret_m.dropna(axis=0, how='any')
ret_m["close"] = [math.log(float(x)) for x in ret_m["close"]]
ret_m['close_down1'] = [math.log(float(x)) for x in ret_m['close_down1']]
ret_m['ret_m'] = (ret_m['close'] - ret_m['close_down1']) * 100
ret_m['date']=[datetime.datetime.strptime(x,'%Y-%m-%d') for x in ret_m['date']]
ret_m['date']=[datetime.datetime.strftime(x,'%Y/%m/%d') for x in ret_m['date']]
print(ret_m)
# 登出系统
bs.logout()
print(ret_m)
#print()
df_3 = pd.merge(factor3,ret_m, on=['date'])

df_2 = pd.merge(df_hml,df_smb, on=['date'])
print(df_2)
df_1 = pd.merge(df_3, df_2, on=['date'])
df_1 = df_1 [["date","code","ret","ret_m","smb","hml"]]


print(df_1)
df_1.to_csv(file_place+'Quantify\\factor\\factor_1_2019.csv', header=True,index=False)






