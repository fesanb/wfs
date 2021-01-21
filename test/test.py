import numpy as np

# trend = 0

def trend_set(v):

	# pos_max = v.index(max(v))
	# pos_min = v.index(min(v))
	# pos_average = v.index(round(sum(v) / len(v), 0))

	t = (sum(v) / len(v)) - v[2]

	if t > 0:
		trend = -1

	if t < 0:
		trend = 1

	if t == 0:
		trend = 0

	trend_set.trend = trend



t = [20,20,21]
t2 = [19,18,17]
t3 = [19,18,18]

trend_set(t3)
print(trend_set.trend)

