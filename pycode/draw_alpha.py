import pandas as pd
import baostock as bs
import warnings
import math
warnings.filterwarnings("ignore")
import datetime
import numpy as np
import matplotlib.pyplot as plt
file_place = 'D:\\'
alpha=pd.read_csv(file_place + 'Quantify\\factor\\factor_alpha_predict.csv')

lg = bs.login()
def get_daily_data(id,start_date_find,end_date_find):
    rs = bs.query_history_k_data_plus(id,
        "date,code,open,close",
        start_date=str(start_date_find), end_date=str(end_date_find),
        frequency="d", adjustflag="3")
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields,index=None)
    result['open_down1'] =  result['open'].shift(periods=1)
    result =  result.dropna(axis=0, how='any')
    result['open'] = [math.log(float(x)) for x in result['open']]
  #  result["close"] = [math.log(float(x)) for x in result["close"]]
    result['open_down1'] = [math.log(float(x)) for x in result['open_down1']]
    result['ret_o'] = ( result['open'] - result['open_down1']) * 100
    result=result[['date','code','ret_o','close']]
    return result

def cal_weight(data):
    data = data.pivot(index='date', columns='code', values='ret_o')
    data = data.reset_index()
    lenn = len(data)
    ret = data.iloc[lenn-1, :]
    day = data.iloc[lenn - 2, :]
    data = data.iloc[0:lenn-3,:]
    return data,ret,day
date=[]


for group in alpha.groupby(['date']):
    date.append(group[0])

date.append('2022/2/2')
date.append('2022/2/2')

i=0
re_p1=[]
date_end1=[]
re_i=[]
for group in alpha.groupby(['date']):
    i = i + 1
    date_end=date[i+1]
    date_end =datetime.datetime.strptime(date_end, '%Y/%m/%d')
    date_start=date_end + datetime.timedelta(days=-30)
    date_end = str(datetime.datetime.strftime(date_end,'%Y-%m-%d'))
    date_start= str(datetime.datetime.strftime(date_start, '%Y-%m-%d'))
    if len(group[1])>1:
        result_code1 = get_daily_data(group[1].iloc[0,0],date_start,date_end)
        result_code2 = get_daily_data(group[1].iloc[1,0],date_start,date_end)
        result_code = result_code1.append(result_code2)
        if len(result_code)>0:
            data, ret,day = cal_weight(result_code)
            cov = data.cov()
            r0= data.mean()
            cov = np.array(cov)
            cov_inv = np.linalg.inv(cov)  # 矩阵求逆
            Ex = np.array([[r0[0]-0.0041], [r0[1]-0.0041]])
            up=np.dot(cov_inv, Ex)
            B = np.dot((np.array([1,1])), cov_inv)
            A = np.dot(B,(np.array([[1],[1]])))
            B = np.dot(B, np.array([[r0[0]], [r0[1]]]))
            down=B-A*0.0014
            weight_p=up/down
            if weight_p[0]<0:
                weight_p[0]=0
                weight_p[1]=1
            if  weight_p[1]<0:
                weight_p[1]=0
                weight_p[0]=1
           # weight_p =[1,0]
            re_p = ret[1] * weight_p[0] + ret[2] * weight_p[1]
            re_p1.append(re_p[0])
            date_end1.append(day[0])
            re_i.append(ret[1])
    else:
        result_code = get_daily_data(group[1].iloc[0,0],date_start,date_end)
        if len(result_code) > 0:
            lenn = len(result_code)
            date_end1.append(result_code.iloc[lenn-2, 0])##T+1的日期
         #   print(result_code)
            ret = result_code.iloc[lenn-1, 2]##T+2的开盘价与T+1的开盘价的收益
            re_p1.append(ret)
            re_i.append(ret)



re1= pd.DataFrame({'date': date_end1, 're_p': re_p1,'re_i':re_i})
print(re1)

del result_code1
del result_code2
rs = bs.query_history_k_data_plus("sh.000001",
    "date,code,open,high,low,close,preclose,volume,amount,pctChg",
    start_date='2019-09-09' , end_date='2019-11-19', frequency="d")
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
ret_m['date']=[datetime.datetime.strftime(x,'%Y-%m-%d') for x in ret_m['date']]
ret_m=pd.DataFrame(ret_m)
##
bs.logout()

df= pd.merge(re1,ret_m, on=['date'])
df=df[["date","re_p","re_i","ret_m"]]
print(df['re_p'].sum())
print(df['re_i'].sum())
print(df['ret_m'].sum())
#print(df)
#plt.plot(df['date'],df['re_p'],df['re_i'],df['ret_m'])
#plt.show()
ax = df.plot(linewidth=2, fontsize=12)
ax.set_ylabel('%')
ax.legend(fontsize=12)
ax.set_xticks([0,15,33,44])
ax.set_xticklabels(["09-09","10-18","11-01","11-19"])
plt.show()

