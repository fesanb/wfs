import numpy as np

def moving_average(a, n=3) :
			ret = np.cumsum(a, dtype=float)
			ret[n:] = ret[n:] - ret[:-n]
			return ret[n - 1:] / n

h = [2000,2001,2000,2002,2003,2002]

trend_res = np.all(np.diff(moving_average(np.array(h), n=4))>0)
print(trend_res)
