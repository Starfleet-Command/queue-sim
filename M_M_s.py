import math


def m_m_s_internal(lamda, miu, s, Cs=None, Cw=None, t=None, n=None):
    Cn = 0
    Pn = 0
    Sum_P0 = 0

    if lamda/(s*miu) > 1:
        return -1

    for sum_n in range(0, s):

        Sum_P0 += (math.pow((lamda/miu), sum_n)/math.factorial(sum_n))

    P0 = 1/(Sum_P0 + (math.pow((lamda/miu), s)/math.factorial(s)) *
            (1/(1-(lamda/(s*miu)))))

    if not n is None:
        if n < s and n >= 1:
            Cn = math.pow((lamda/miu), n)/math.factorial(n)

        else:
            Cn = math.pow((lamda/miu), n) / \
                (math.factorial(s)*math.pow(s, (n-s)))

        if n < s and n >= 0:
            Pn = (math.pow((lamda/miu), n)/math.factorial(n)) * P0

        elif n >= s:
            Pn = Cn * P0

        elif n == 0:
            Pn = P0
    else:
        Cn = 0
        Pn = 0

    rho = lamda/(s*miu)

    Lq = (P0*math.pow((lamda/miu), s)*rho) / \
        (math.factorial(s)*math.pow((1-rho), 2))

    Wq = Lq/lamda

    W = Wq + (1/miu)

    L = lamda*W

    if not Cs is None and not Cw is None:
        Ct = Lq*Cw+s*Cs
        Cl = L*Cw+s*Cs
    else:
        Ct = 0
        Cl = 0

    if not t is None:
        Wt = math.pow(math.e, -miu*t) * (1+(math.pow(s*rho, s)*P0*(1-math.pow(
            math.e, -miu*t*(s-1-s*rho))))/(math.factorial(s)*(1-rho)*(s-1-s*rho)))

        Wqt = ((math.pow(s*rho, s)*P0)/(math.factorial(s)*(1-rho))) * \
            math.pow(math.e, -s*miu*t*(1-rho))

    else:
        Wt = 0.0
        Wqt = 0.0

    res = {}
    res["P\u2080"] = P0
    res["P\u2099"] = Pn
    res["\u03C1"] = rho
    res["L"] = L
    res["W"] = W
    res["Wq"] = Wq
    res["Lq"] = Lq
    res["Ct"] = Ct
    res["Cl"] = Cl
    res["Wt"] = Wt
    res["Wqt"] = Wqt
    res["C\u2099, 0<=n<s"] = "( ( (" + str(lamda) + "/" + \
        str(miu) + ")^ n )" + "/" + "n!) " + "*" + str(P0)
    res["C\u2099, n>=s"] = "( (" + str(lamda) + "/" + str(miu) + ")^n /" + \
        "(" + str(s) + "! * " + str(s) + "^(n-" + str(s)+")) )" + "*" + str(P0)

    return res


def mms(lamda, miu, s, Cs=None, Cw=None, t=None, n=None):
    result = m_m_s_internal(lamda, miu, s, Cs, Cw, t, n)

    return result


#resultado = mms(120, 80, 3, 20, 48, 0.05, 0)
# print(resultado)
