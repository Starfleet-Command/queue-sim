import math

def get_mmsk(lam, miu, s, k):
	sum_1 = 0
	sum_2 = 0
	
	for n in range(0, s+1):
		sum_1 = sum_1 + (math.pow(lam / miu, n) / math.factorial(n))

	for n in range(s+1, k+1):
		sum_2 = sum_2 + math.pow(lam / (miu * s), n-s)
	
	mid = (math.pow(lam / miu, s) / math.factorial(s))

	p0 = 1 / (sum_1 + (mid * sum_2))
	pk = (math.pow(lam / miu, k) / (math.factorial(s) * math.pow(s, k-1))) * p0

	rho = lam / (s * miu)

	lq_1 = (p0 * math.pow(lam / miu, s) * rho) / (math.factorial(s) * math.pow(1 - rho, 2))
	lq_2 = 1 - math.pow(rho, k - s) - ((k - s) * math.pow(rho, k - s) * (1 - rho))
	lq = lq_1 * lq_2

	lam_e = lam * (1 - pk)
	wq = lq / lam_e
	w = wq + (1 / miu)
	l = lam_e * w

	#TODO regresar los valores en una lista como el M_M_s porfa
	# tiene que ser [p0, Pn (o pk como esta aqui), Cn, rho, l, w, wq, lq]

	print("p0: " + str(p0))
	print("pk: " + str(pk))
	print("lq: " + str(lq))
	print("lam_e: " + str(lam_e))
	print("wq: " + str(wq))
	print("w: " + str(w))
	print("l: " + str(l))

	
