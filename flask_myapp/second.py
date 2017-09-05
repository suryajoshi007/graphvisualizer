@decor
def fact(n):
	print("in fact function")
	if n==1:
		return n
	return n*fact(n-1)

fact(6)