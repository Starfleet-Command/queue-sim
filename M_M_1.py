import math
def get_m_m_1 (lamda, miu, n, Cs=None, Cw=None):
    rho = lamda/miu
    P0 = 1 - rho
    Cn= math.pow(rho, n)
    Pn=(1 - rho)*P0
    Lq= math.pow(lamda, 2)/ miu*(miu-lamda)
    L= lamda/ (miu-lamda)
    Wq= lamda/ miu*(miu-lamda)
    W= 1/(miu-lamda)

    if Cw and Cs:
        Ct = Cw*Lq + 1*Cs

        #print("P0", P0)
        #print("Pn", Pn)
        #print("Cn", Cn)
        #print("rho", rho)
        #print("L", L)
        #print("W", W)
        #print("Lq", Lq)
        #print("Wq", Wq)
        #print("Ct", Ct)
        return list([P0, Pn, Cn, rho, L, W, Wq, Lq, Ct])
    else:
        
        return list([P0, Pn, Cn, rho, L, W, Wq, Lq])

# mm1 = get_m_m_1(2.0, 3.0, 2.0, 12.0, 15.0)
# print(mm1)
