import math

def get_m_d_1(lamda, miu, n, Cs=None, Cw=None):
    rho = lamda/miu
    P0 = 1 - rho
    Pn = math.pow(rho, n) * P0

    Cn = -1

    Lq = (math.pow(rho, 2))/(2*(1-rho))

    L = rho + Lq

    Wq = Lq/lamda

    W = Wq + 1/miu

    if Cw and Cs:
        Ct = Cw*Lq + Cs*1
        return list([P0, Pn, Cn, rho, L, W, Lq, Wq, Ct])
    else:
        return list([P0, Pn, Cn, rho, L, W, Lq, Wq])


# md1 = get_m_d_1(3.0, 5.0, 1.0)
# print(md1)
