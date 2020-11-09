import math


def m_m_s_internal(lamda, miu, n, s, Cs=None, Cw=None):
    Cn = 0
    Pn = 0
    Sum_P0 = 0

    if lamda/(s*miu) > 1:
        return -1

    if n <= s and n >= 1:
        Cn = math.pow((lamda/miu), n)/math.factorial(n)

    else:
        Cn = math.pow((lamda/miu), n)/(math.factorial(s)*math.pow(s, (n-s)))

    for sum_n in range(0, s):
        print((math.pow((lamda/miu), sum_n)/math.factorial(sum_n)))
        Sum_P0 += (math.pow((lamda/miu), sum_n)/math.factorial(sum_n))
        print(Sum_P0)

    P0 = 1/(Sum_P0 + (math.pow((lamda/miu), s)/math.factorial(s)) *
            (1/(1-(lamda/(s*miu)))))

    if n < s and n >= 0:
        Pn = (math.pow((lamda/miu), n)/math.factorial(n)) * P0

    else:
        Pn = Cn * P0

    rho = lamda/(s*miu)

    Lq = (P0*math.pow((lamda/miu), s)*rho) / \
        (math.factorial(s)*math.pow((1-rho), 2))

    Wq = Lq/lamda

    W = Wq + (1/miu)

    L = lamda*W


    Ct = Lq*Cw+s*Cs


    print("P0", P0)
    print("Pn", Pn)
    print("Cn", Cn)
    print("rho", rho)
    print("L", L)
    print("W", W)
    print("Wq", Wq)
    print("Lq", Lq)
    print("Ct", Ct)

    res = {}
    res["P\u2080"] = P0
    res["P\u2099"] = Pn
    res["C\u2099"] = Cn
    res["\u03C1"] = rho
    res["L"] = L
    res["W"] = W
    res["Wq"] = Wq
    res["Lq"] = Lq
    res["Ct"] = Ct

    return res


def mms(lamda, miu, n, s, Cs=None, Cw=None):
    result = m_m_s_internal(lamda, miu, n, s, Cs, Cw)

    return result


# lambda, miu, n, s
resultado = mms(120, 80, 0, 3, 20, 48)
print(resultado)
