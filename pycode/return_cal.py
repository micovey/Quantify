import pandas as pd
import math

print('请输入地址')
global file_place
file_place='D:\\'
fff=file_place+'\\Quantify\\daily\\daily'+str(2019)+'.csv'

##计算收益率
def cal_return(group):
    group=pd.DataFrame(group[1])##提取数据框
    group['close_down1']= group['close'].shift(periods=1)
    group = group.dropna(axis=0, how='any')
    group["close"] = [math.log(x)  for x in group["close"]]
    group['close_down1'] = [math.log(x) for x in group['close_down1']]
    group['ret'] = (group['close']-group['close_down1'])*100
    group=group[['date','code','quarter','year','ret','marketvalue']]
    return(group)

daily_data = pd.read_csv(file_place+'Quantify\\daily\\daily'+str(2019)+'.csv')
returndata=pd.DataFrame(columns=['date','code','quarter','year','ret','marketvalue'])
g=pd.DataFrame(columns=['date','code','quarter','year','ret','marketvalue'])
print(g)
for group in daily_data.groupby(['code']):
    g=cal_return(group)
    returndata=returndata.append(g)
    print(group[0])
#eturndata.to_csv(file_place+'Quantify\\daily\\daily_ret'+str(2019)+'.csv', header=True,index=False)

