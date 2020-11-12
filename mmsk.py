import math


def get_mmsk(lam, miu, s, k, cw=None, cs=None, n=None):
	sum_1 = 0
	sum_2 = 0
	
	for n in range(0, s+1):
		sum_1 = sum_1 + (math.pow(lam / miu, n) / math.factorial(n))

	for n in range(s+1, k+1):
		sum_2 = sum_2 + math.pow(lam / (miu * s), n-s)
	
	mid = (math.pow(lam / miu, s) / math.factorial(s))

	p0 = 1 / (sum_1 + (mid * sum_2))
	pk = (math.pow(lam / miu, k) / (math.factorial(s) * math.pow(s, k-1))) * p0

	pn_less_s = "((" + str(lam) + "/" + str(miu) + ")^n/n!) * " + str(p0)
	pn_s_to_k = "((" + str(lam) + "/" + str(miu) + ")^n/" + str(s) + "!" + str(s) + "^(n-" + str(s) + ")) * " + str(p0)
	pn_more_k = str(0)

	if(n):
		if(n <= s):
			pn = (math.pow(lam / miu, n) / math.factorial(n)) * p0
		elif(n <= k):
			pn = (math.pow(lam / miu, n) / (math.factorial(s) * math.pow(s, n-s))) * p0
		else:
			pn = 0

	rho = lam / (s * miu)

	lq_1 = (p0 * math.pow(lam / miu, s) * rho) / (math.factorial(s) * math.pow(1 - rho, 2))
	lq_2 = 1 - math.pow(rho, k - s) - ((k - s) * math.pow(rho, k - s) * (1 - rho))
	lq = lq_1 * lq_2

	lam_e = lam * (1 - pk)
	wq = lq / lam_e
	w = wq + (1 / miu)
	l = lam_e * w

	res = {}

	if(cw and cs):
		ctlq = (lq * cw) + (s * cs)
		ctl = (l * cw) + (s * cs)

	res["P\u2080"] = round(p0, 4)
	res["P\u2096"] = round(pk, 4)

	res["P\u2099, n<=s"] = pn_less_s
	res["P\u2099, s<n<=k"] = pn_s_to_k
	res["P\u2099, n>k"] = pn_more_k

	if(n):
		res["P" + str(n)] = round(pn, 4)

	res["\u03c1"] = round(rho, 4)
	res["L"] = round(l, 4)
	res["W"] = round(w, 4)
	res["Wq"] = round(wq, 4)
	res["Lq"] = round(lq, 4)

	if(cw and cs):
		res["Ct, with Lq"] = round(ctlq, 2)
		res["Ct, with L"] = round(ctl, 2)

	return res
