import build
from collections import defaultdict
import json
import numpy as np
import os
import pylab as pl

exp_name = "SlidingBig"
states_dir = build.data_name("tase/states/%s"%exp_name)
print "states_dir is ",states_dir
#states_dir = "%s/states/%s/" % (defs.exp_data_dir(), exp_name)
#perf_file = "%s/states/perf2010-03-07-0.txt" % defs.exp_data_dir()

#marg_lls = []
#marg_emp_lls = []
#for l in open(perf_file):
#  tokens = l.split(" ")
#  marg_ll = float(tokens[4])
#  ecll = float(tokens[5])
#  entropy = float(tokens[6])
#  marg_lls.append(marg_ll)
#  marg_emp_lls.append(ecll + entropy)

#required_states = frozenset(range(186))
required_states = frozenset([186, 187, 188, 411, 1104, 1105, 1171, 1172, 1201, 1209])
#required_states = frozenset([28969,28971,28985,28999,29001])

partial_state_fnames = sorted([s for s in os.listdir(states_dir) if s.startswith("full-2010-10-12") and s.endswith(".txt")])


class GammaState(object):
  def __init__(self, k, theta):
    self.k = k
    self.theta = theta
  def __repr__(self):
    return "GS[k=%f,theta=%f]" % (self.k, self.theta)

states = defaultdict(list)

for partial_state_fname in partial_state_fnames:
  fname = "%s/%s" % (states_dir, partial_state_fname)
  print fname
  for l in open(fname):
    try:
      dct = json.loads(l.replace("_1", "nodeId").replace("_2", "state"))
      linkid = int(dct["nodeId"])
      if linkid in required_states:
        k = float(dct["state"]["k"])
        theta = float(dct["state"]["theta"])
        gs = GammaState(k, theta)
        states[linkid].append(gs)
    except:
      pass

#fig = pl.figure(0)
#ax = fig.gca()
#for state_list in states.values():
#  ks = [gs.k for gs in state_list]
#  thetas = [gs.theta for gs in state_list]
#  ax.plot(ks, thetas)

import matplotlib.ticker as ticker
fig = pl.figure(1)
ax = fig.gca()
for state_list in states.values():
  means = [gs.k * gs.theta for gs in state_list]
  ax.plot(means)

N = len(partial_state_fnames)
ind = np.arange(N)  # the evenly spaced plot indices

def format_date(x, pos=None):
    thisind = np.clip(int(x + 0.5), 0, N - 1)
    return partial_state_fnames[thisind][16:24]

ax.set_title("Mean travel time for a few links")
ax.set_ylabel("Mean TT (secs)")
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
fig.autofmt_xdate()
build.save_figure(fig, "figures-socc/example")
#fig.show()
