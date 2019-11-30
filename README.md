### 数据及代码说明
</br>
注意！下载完的文件夹一定要命名为Quantify，不要为Quantify-master等等</br>
数据来源：baostock：http://baostock.com/</br>
默认存储路径：D盘</br>
默认将daily2019.csv存在D:\Quantify\daily</br>
</br>
##### 代码说明
</br>
daily.py：自动更新规定时间内的日度数据，可以自行修改数据期间。默认为半年前至当日。以便后续分析</br>
factor.py :下载三因子所需数据，但日期需要自行更改，一般需要两年，6月底分组</br>
factor_cal.py:将股票进行分组，以便后续计算因子</br>
return_cal.py：计算对数收益率</br>
factor_merge.py: 收益率、因子等将匹配</br>
alpha.py： 计算滚动α</br>
pre_alpha.py： 计算滚动预测α，选出每日最合适的股票（<=2个)</br>
未完待续……</br>

</br>
stochastic.py 模拟随机游走、布朗运动，计算Hurst指数
