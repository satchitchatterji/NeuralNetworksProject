





import matplotlib.pyplot as plt
import numpy as np

file_ref = '20210603T1435'
draw_type = 'mean'
# draw_type = 'min'

draw_sd = True
draw_sd = False


f = open(f'tests/{draw_type}_scores_{file_ref}.txt', 'r').readlines()[0].strip()
f = f.replace('[', "")
f = f.replace(']', "")
vals = np.array([float(x) for x in f.split(',')])

plt.plot(vals, color = 'red', label = draw_type)

if draw_sd:
	f = open(f'tests/sd_scores_{file_ref}.txt', 'r').readlines()[0].strip()
	f = f.replace('[', "")
	f = f.replace(']', "")
	sds = np.array([float(x) for x in f.split(',')])

	plt.plot(vals+sds, color = 'green', label = 'stddev')
	plt.plot(vals-sds, color = 'green')

plt.legend()
plt.show()