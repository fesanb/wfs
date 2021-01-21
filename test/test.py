import numpy as np

def trend(h):

	def moving_average(a, n=3) :
				ret = np.cumsum(a)
				ret[n:] = ret[n:] - ret[:-n]
				return ret[n - 1:] / n

	trend.trend_res = np.all(np.diff(moving_average(np.array(h), n=4))>0)

# h = [41,41,41,43,44,44,43,43,38,38]
h = [41,41,41,43,44,44,45,46,46,46]


trend(h)
if trend.trend_res == 0:
	print("False")

if trend.trend_res == 1:
	print("True")
