import pandas as pd
import numpy as np
###分组
file_place='D:\\'##自行更改

def clear_data(data_prepare):
    ddd=file_place+'\\Quantify\\factor\\factor_copy'+str(2019)+'.csv'
    data_prepare["book_market"] = [np.nan if x == "" or x >1000 else float(x) for x in data_prepare["book_market"]]
    data_prepare["marketvalue"] = [np.nan if x == "" else float(x) for x in data_prepare["marketvalue"]]
    data_prepare=data_prepare.dropna(axis=0, how='any')
    data_prepare=data_prepare[["code","book_market","marketvalue","year"]]
    return(data_prepare)

year_list=['2018','2019']
for year in year_list:
    fff=file_place+'\\Quantify\\factor\\factor'+str(year)+'.csv'
    ddd=file_place+'\\Quantify\\factor\\factor_sort'+str(year)+'.csv'
    data_prepare = pd.read_csv(fff)
    data_prepare = clear_data(data_prepare)
    cut_smb=data_prepare["marketvalue"].quantile(q=0.5)
    data_prepare["smb_dum"] = [1 if x < cut_smb else 0 for x in data_prepare["marketvalue"]]###小市值取值为1，大为0
    cut_hml_l = data_prepare["book_market"].quantile(q=0.3)
    cut_hml_2 = data_prepare["book_market"].quantile(q=0.7)
    data_prepare["hml_dum_1"] = [1 if x < cut_hml_l else 0 for x in data_prepare["book_market"]]  ###小账面市值比为2
    data_prepare["hml_dum_2"] = [1 if x < cut_hml_2 else 0 for x in data_prepare["book_market"]]  ###大账面市值比为0
    data_prepare["hml_dum"]=data_prepare["hml_dum_2"]+data_prepare["hml_dum_1"]
    data_prepare=data_prepare[["code","smb_dum","hml_dum"]]
    data_prepare.to_csv(ddd, header=True,index=False)