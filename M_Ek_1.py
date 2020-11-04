import math

def get_m_ek_1(lamda, miu, n, k):
    rho = lamda/miu
    P0 = 1 - rho
    Pn = math.pow(rho, n) * P0

    Cn = -1

    Lq = ((1+k)/(2*k)) * ((math.pow(lamda, 2))/(miu*(miu-lamda)))
    
    Wq = Lq/lamda

    W = Wq + 1/miu

    L = lamda * W

    return list([P0, Pn, Cn, rho, L, W, Lq, Wq])


# mek1 = get_m_ek_1(3.0, 5.0, 1.0, 4.0)
# print(mek1)
