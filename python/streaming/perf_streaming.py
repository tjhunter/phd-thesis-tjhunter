from defs import save_path
import pylab as pl
import numpy as np
import matplotlib

num_nodes = [5, 10, 20, 40, 80]
data_rate_ratio = [0.02, 0.04, 0.08, 0.16, 0.32]
data_rate = [i * 5350.0 for i in data_rate_ratio]

matplotlib.rcParams.update({'font.size': 18})

fig = pl.figure(0, figsize=(6,4))
ax = fig.gca()
ax.plot(num_nodes, data_rate, 'k-o')
ax.set_ylabel("Observations per second")
ax.set_xlabel("Number of nodes")
for loc, spine in ax.spines.items():
    if loc in ['right','top']:
        spine.set_color('none') # don't draw spine
ax.set_xticks(num_nodes)
ax.set_xlim(0,85)

fig.savefig("%s/perf_streaming.pdf"%save_path(), bbox_inches='tight')
fig.savefig("%s/perf_streaming.svg"%save_path(), bbox_inches='tight')