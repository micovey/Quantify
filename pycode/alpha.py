import pandas as pd
import statsmodels.api as sm

file_place='D:\\'
factordata = pd.read_csv(file_place+'Quantify\\factor\\factor_1_2019.csv')
#CSMAR数据显示，无风险收益率近期均为0.0041%（日度）
cal_len=60##自行修改，计算α所需数据的长度
factordata["Ex_r"]=factordata["ret"]-0.0041#证券超额收益
factordata["Ex_rm"]=factordata["ret_m"]-0.0041#市场组合超额收益
p=[]
code=[]
alpha_c=[]
date1=[]
for group in factordata.groupby(['code']):
    code_store=group[0]
    print(group[0])#输出股票代码，提示进度
    g=group[1]#每一个股票的数据
    roll_len = len(g) - cal_len##滚动长度
    for i in range(0, roll_len+1):
    #    print(group[1])
        g1= g.iloc[0 +i:cal_len +i, :]#提出设定长度的数据，不断滚动，得到滚动α
      #  print(g1)
     #   print(g1.iloc[cal_len-1, 0])
        date1.append(g1.iloc[cal_len-1, 0])
        X = g1[['Ex_rm', 'smb','hml']]
        y = g1['Ex_r']
        est = sm.OLS(y, sm.add_constant(X),M=sm.robust.norms.HuberT()).fit()#考虑稳健性的p值
        print(est.summary()) #可查看每一个模型结果
        p.append(est.pvalues.iloc[0])
        alpha_c.append(est.params.iloc[0])
        code.append(code_store)
df_store= pd.DataFrame({'code': code,'date':date1,  'p':p, 'alpha_c': alpha_c})
df_store.to_csv(file_place+'Quantify\\factor\\factor_alpha_2019.csv', header=True,index=False)

#   print(dir(est)) 查看如何调用p值的数据
