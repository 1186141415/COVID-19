
#写出SIR模型的函数
def SIR(y,t,beta,gamma):
    S,I,R = y
    dSdt = -S*(I/(S+I+R))*beta
    dIdt = S*(I/(S+I+R))*beta-gamma*I
    dRdt = gamma*I
    return [dSdt,dIdt,dRdt]