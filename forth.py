
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
