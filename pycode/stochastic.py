import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
##计算频率
def count_elements(seq):
    hist = {}
    for i in seq:
        hist[i] = hist.get(i, 0) + 1
    return hist

def random_walk(length):
    line =[]
    line.append(0)
    for i in range (1,length):
        each_step = 2*np.random.binomial(1,0.5,1)-1
        add=float(line[i-1]+each_step)
        line.append(add)
    return line

def Brown_movement(length):
    line =[]
    line.append(float(0))
    for i in range (1,length):
        each_step = float((2*np.random.binomial(1,0.5,1)-1)/math.sqrt(length))
        add=float(line[i-1]+each_step)
        line.append(add)
    return line

def Brown_movement_geometric(length,mu):
    line =[]
    line.append(float(0))
    for i in range (1,length):
        each_step = float((2*np.random.binomial(1,0.5,1)-1)/math.sqrt(length))
        add=float(line[i-1]+each_step+mu*i)
        line.append(add)
    return line

def Hurst(data):
    pannel_num = 8
    ARS =[]
    lag =[]
    for i in range(pannel_num):
        size = np.size(data) // (2 ** i)
        lag.append(size)
        panel = {}
        for sub_pannel_num in range((2 ** i)):
            panel["sub_pannel:"+str(sub_pannel_num)] = data[sub_pannel_num*size:(sub_pannel_num+1)*size]
        panel = pd.DataFrame(panel)
        mean = panel.mean()
        Dev = (panel - mean).cumsum()
        sigma = panel.std()
        RS = (Dev.max() - Dev.min())/sigma
        ARS.append(RS.mean())

    lag = np.log10(lag)
    ARS = np.log10(ARS)
    hurst_exponent = np.polyfit(lag, ARS, 1)
    hurst = hurst_exponent[0]
    return hurst
###随机游走
##模拟4条
y=np.sqrt(np.array(range(101)))
for i in range(0,4):
    walk=random_walk(100)
    plt.plot(walk)
plt.plot(y,'k')
plt.plot(-y,'k')
plt.plot(2*y,'k')
plt.plot(-2*y,'k')
plt.grid(True)
plt.show()
sum=[]
##画出100条，100s后的分布
for i in range(0,100):
    walk=random_walk(100)
    sum.append(walk[-1])
plt.hist(sum, np.array(range(-30,31)))
plt.show()

###布朗运动
##模拟4条
y1=np.sqrt(np.array(range(1001))/1000)
y2=2*np.sqrt(np.array(range(1001))/1000)
for i in range(0,4):
    walk=Brown_movement(1000)
    plt.plot(walk)
plt.plot(y1,'k')
plt.plot(-y1,'k')
plt.plot(y2,'k')
plt.plot(-y2,'k')#
plt.grid(True)
plt.xticks(range(0,1001,1000),{"0","1"})
plt.show()
##画出10000条，1s后的分布
nnn=10000
sum = []
for i in range(0,nnn):
    walk=Brown_movement(1000)
    sum.append(walk[-1])
b=np.array(range(-90,91))/30
plt.hist(sum, b)
plt.show()

###Hurst指数
ret=[]
price=[]
ret.append(float(0))
price.append(float(0))
for i in range(1,1000):
    walk=Brown_movement(1000)
    ret.append(float(walk[-1]))
    price.append(float(walk[-1])+price[i-1])
print(Hurst(ret))
print(Hurst(price))
plt.plot(ret,'k')
plt.show()
plt.plot(price,'k')
plt.show()


###几何布朗运动
for i in range(0,4):
    walk=Brown_movement_geometric(1000,0.00001)
    plt.plot(walk)
plt.grid(True)
plt.xticks(range(0,1001,1000),{"0","1"})
plt.show()