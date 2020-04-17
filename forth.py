import numpy as np
from scipy.integrate import odeint

#绘图
import matplotlib.pyplot as plt
#在jupyter中设置行内显示
#%maplotlib inline

#用pandas导入数据
import pandas as pd

#写出SIR模型的函数
def SIR(y,t,beta,gamma):
    S,I,R = y
    dSdt = -S*(I/(S+I+R))*beta
    dIdt = S*(I/(S+I+R))*beta-gamma*I
    dRdt = gamma*I
    return [dSdt,dIdt,dRdt]

#为SIR模型设置初始值
#设置人群总人数为N
N = 58000000
#设置初始时的感染人数为239
I0 = 239
#设置初始时的恢复人数R0为31（恢复人数指不会再传染给他人，所以这里指恢复和死亡人数的总和）
R0 = 31
#所以初始易感人群总人数 = 总人数 - 初始感染人数 - 初始治愈人数
S0 = N-I0-R0
#设置初始值
y0 = [S0,I0,R0]

#设置疫情的时间跨度为60天或360天
t = np.linspace(1,360,360)

#设置beta的值等于0.125
beta = 0.125

#设置gamma的值等于0.05
gamma = 0.05

#求解，每次改完时间要从新计算solution
solution = odeint(SIR, y0, t, args=(beta, gamma))

#显示用正常10进制格式
np.set_printoptions(suppress=True)
#显示前4行结果
#solution[0:4,0:3]

#绘图
fig, ax = plt.subplots(facecolor='w', dpi=100)

for data, color, label_name in zip([solution[:,0] ,solution[:,1], solution[:,2]], ['b','r', 'g'],['susceptible','infectious','recovered']):
    ax.plot(t, data, color, alpha = 0.5, lw=2, label=label_name)

ax.set_xlabel('Time/days')
ax.set_ylabel('Number')
ax.legend()
ax.grid(axis='y')
plt.box(False)
#plt.show()

#导入数据
data = pd.read_csv('alltime_province_2020_04_04.csv')
#选择数据中关于湖北省的数据
hubei = data[data['name']=='湖北']

infectious_real = hubei['total_confirm']-hubei['total_heal']-hubei['total_dead']
recovered_real = hubei['total_heal']+hubei['total_dead']
susceptible = N-infectious_real-recovered_real
