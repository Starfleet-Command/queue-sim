import math


def get_m_g_1(lamda, miu, sigma, Cs=None, Cw=None, n=None):
    rho = lamda/miu
    if rho >= 1:
        return -1
    P0 = 1 - rho
    pn = "((" + str(lamda) + "/" + str(miu) + ")^n/n!) * " + str(P0)

    Lq = ((math.pow(lamda, 2) * math.pow(sigma, 2)) +
          math.pow(rho, 2))/(2*(1-rho))

    L = rho + Lq

    Wq = Lq/lamda

    W = Wq + 1/miu

    res = {}

    if Cw and Cs:
        Ctlq = Cw*Lq + Cs*1
        Ctl = Cw*L + Cs*1

    res["P\u2080"] = round(P0, 4)
    res["P\u2099, n"] = pn

    if(n):
        Pn = math.pow(rho, n) * P0
        res["P" + str(n)] = round(Pn, 4)

    res["\u03c1"] = round(rho, 4)
    res["L"] = round(L, 4)
    res["W"] = round(W, 4)
    res["Wq"] = round(Wq, 4)
    res["Lq"] = round(Lq, 4)

    if(Cw and Cs):
        res["Ct, with Lq"] = round(Ctlq, 2)
        res["Ct, with L"] = round(Ctl, 2)

    return res

# mg1 = get_m_g_1(3.0, 5.0, 0.1)
# print(mg1)
