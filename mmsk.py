import math

def get_mmsk(lam, miu, s, k, cw=0, cs=0):
	mmsk_list = []
	
	sum_1 = 0
	sum_2 = 0
	
	for n in range(0, s+1):
		sum_1 = sum_1 + (math.pow(lam / miu, n) / math.factorial(n))

	for n in range(s+1, k+1):
		sum_2 = sum_2 + math.pow(lam / (miu * s), n-s)
	
	mid = (math.pow(lam / miu, s) / math.factorial(s))

	p0 = 1 / (sum_1 + (mid * sum_2))
	pk = (math.pow(lam / miu, k) / (math.factorial(s) * math.pow(s, k-1))) * p0

	cn_less_s = "(" + str(lam) + "/" + str(miu) + ")^n/n!"
	cn_s_to_k = "(" + str(lam) + "/" + str(miu) + ")^n/s!s^(n-s)"
	cn_more_k = str(0)

	pn_less_s = "((" + str(lam) + "/" + str(miu) + ")^n/n!) * " + str(p0)
	pn_s_to_k = "((" + str(lam) + "/" + str(miu) + ")^n/s!s^(n-s)) * " + str(p0)
	pn_more_k = str(0)

	rho = lam / (s * miu)

	lq_1 = (p0 * math.pow(lam / miu, s) * rho) / (math.factorial(s) * math.pow(1 - rho, 2))
	lq_2 = 1 - math.pow(rho, k - s) - ((k - s) * math.pow(rho, k - s) * (1 - rho))
	lq = lq_1 * lq_2

	lam_e = lam * (1 - pk)
	wq = lq / lam_e
	w = wq + (1 / miu)
	l = lam_e * w

	ct = (lq * cw) + (s * cs)

	mmsk_list.append(str("%.4f" % round(p0, 4)))
	mmsk_list.append(str("%.4f" % round(pk, 4)))

	mmsk_list.append(cn_less_s)
	mmsk_list.append(cn_s_to_k)
	mmsk_list.append(cn_more_k)

	mmsk_list.append(pn_less_s)
	mmsk_list.append(pn_s_to_k)
	mmsk_list.append(pn_more_k)

	mmsk_list.append(str("%.4f" % round(rho, 4)))
	mmsk_list.append(str("%.4f" % round(l, 4)))
	mmsk_list.append(str("%.4f" % round(w, 4)))
	mmsk_list.append(str("%.4f" % round(wq, 4)))
	mmsk_list.append(str("%.4f" % round(lq, 4)))

	if(ct > 0):
		mmsk_list.append(str("%.2f" % round(ct, 2)))

	# Orden de la lista [P0, Pk, Cn...n<=s, Cn...s<n<=k, Cn...n>k, Pn...n<=s, Pn...s<n<=k, Pn...n>k, rho, L, W, Wq, Lq, Ct]
	return mmsk_list
	
