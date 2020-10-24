import math


def m_m_s_internal(lamda, miu, n, s):
    Cn = 0
    Pn = 0
    Sum_P0 = 0

    if lamda/miu > 1:
        return -1

    if n < s and n > 0:
        Cn = math.pow((lamda/miu), n)/math.factorial(n)

    elif n >= s:
        Cn = math.pow((lamda/miu), n)/(math.factorial(s)*math.pow(s, (s-n)))

    for sum_n in range(0, s-1):
        Sum_P0 = Sum_P0 + (math.pow((lamda/miu), sum_n)/math.factorial(n))

    P0 = 1/(Sum_P0 + (math.pow((lamda/miu), s)/math.factorial(s)) *
            (1/(1-(lamda/(s*miu)))))

    if n < s and n >= 0:
        Pn = (math.pow((lamda/miu), n)/math.factorial(n)) * P0

    elif n >= s:
        Pn = Cn * P0

    rho = lamda/(s*miu)

    Lq = (P0*math.pow((lamda/miu), s)*rho) / \
        (math.factorial(s)*math.pow((1-rho), 2))

    Wq = Lq/lamda

    W = Wq + (1/miu)

    L = lamda*W

    return list([P0, Pn, Cn, rho, L, W, Wq, Lq])


def mms(lamda, miu, n, s):
    result = m_m_s_internal(lamda, miu, n, s)

    return result


#resultado = mms(3, 5, 2, 4)
# print(resultado)
