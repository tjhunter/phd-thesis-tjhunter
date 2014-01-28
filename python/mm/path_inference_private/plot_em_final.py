import build

import numpy as np
from collections import defaultdict
import pickle
import random
random.seed = 1
from mm.path_inference_private.proj_templates import get_em_evaluation_fnames, get_evaluation_em_data_file
from mm.path_inference_private.evaluation import LEARNING_METHOD_IDX, METRIC_NAME_IDX, STRAT_NAME_IDX
from mm.path_inference_private.plot_utils import *
import pylab as pl
import matplotlib.pyplot as plt

__author__ = 'tjhunter'

def get_all_eval_em(res):
  all_eval = defaultdict(list)
  for (_, _res, _batch_idx) in get_em_evaluation_fnames(res=res):
    fin = get_evaluation_em_data_file(res=_res, batch_idx=_batch_idx)
    data = pickle.load(fin)
    fin.close()
    for (key, val) in data.iteritems():
      all_eval[key].append(val)
  return all_eval

res = 60
all_em_evals = get_all_eval_em(res=res)
all_evals = {}
all_evals[res] = get_all_eval(res=res)
all_evals[res].update(all_em_evals)

num_boot_samples = 1000
strategy = 'VITERBI'

learning_display =  {'most_likely_simple' : 'MaxLL - simple', \
          'em_simple' : 'EM - simple', \
          'most_likely_fancy' : 'MaxLL - complex', \
          'em_large_simple_1' : 'EM - simple (large)', \
          'em_large_fancy_1' : 'EM - complex (large)', \
          }

learning_methods = list(learning_display.keys())
learning_methods.sort()
#learning_methods = ['most_likely_simple', 'most_likely_fancy', 'em_simple', 'em_large_simple_1', 'em_large_simple_2', 'em_large_simple_3', 'em_large_simple_4', 'em_large_simple_5', 'em_large_fancy_1', 'em_large_fancy_2', 'em_large_fancy_3', 'em_large_fancy_4', 'em_large_fancy_5']
num_methods = len(learning_methods)


strategy = 'VITERBI'
data_by_method = []
median_vals = []
mean_vals = []
lower_percentile = []
upper_percentile = []
for learning in learning_methods:
    data = get_true_point_by_strat(all_eval=all_evals[res],
                                   learning_method=learning)[strategy]
    data_by_method.append(data)
    stat_dis = bootstrap_percent_wrong(data, num_boot_samples)
    median_vals.append(stat_dis[int(num_boot_samples*0.5)])
    mean_vals.append(np.mean(stat_dis))
    lower_percentile.append(stat_dis[int(num_boot_samples*0.20)])
    upper_percentile.append(stat_dis[int(num_boot_samples*0.80)])

fig = pl.figure(1, figsize=(10,8))
fig.clf()
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.30)
xs = np.arange(num_methods)+1
plot_error_bar(ax, xs, mean_vals, lower_percentile, upper_percentile, fmt='ko')
ax.set_xlim(0.5, num_methods+0.5)
ax.set_ylim(0.05, 0.07)
ax.set_title("Comparison of point assignment errors for 1-minute sampling intervals \n (Viterbi reconstruction)")
ax.set_xticks(xs)
xtickNames = ax.set_xticklabels([learning_display[method_name] for method_name in learning_methods])
plt.setp(xtickNames, rotation=60, fontsize=12)
ax.set_xlabel("Learning method")
ax.set_ylabel("Proportion of false point assignments")
build.save_figure(fig,"figures-pif/em_true_points_percentage")
#fig.savefig("%s/em_true_points_percentage.pdf"%saving_dir())

''' TRUE PATHS
'''

strategy = 'VITERBI'
median_vals = []
mean_vals = []
lower_percentile = []
upper_percentile = []
for learning in learning_methods:
    data = get_true_path_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    stat_dis = bootstrap_percent_wrong(data, num_boot_samples)
    median_vals.append(stat_dis[int(num_boot_samples*0.5)])
    mean_vals.append(np.mean(stat_dis))
    lower_percentile.append(stat_dis[int(num_boot_samples*0.20)])
    upper_percentile.append(stat_dis[int(num_boot_samples*0.80)])

fig = pl.figure(2, figsize=(10,8))
fig.clf()
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.1, right=0.98, top=0.9, bottom=0.30)
xs = np.arange(num_methods)+1
plot_error_bar(ax, xs, mean_vals, lower_percentile, upper_percentile, fmt='ko')
ax.set_xlim(0.5, num_methods+0.5)
ax.set_title("Comparison of path assignment errors for 1-minute sampling intervals \n (Viterbi reconstruction)")
ax.set_xticks(xs)
xtickNames = ax.set_xticklabels([learning_display[method_name] for method_name in learning_methods])
plt.setp(xtickNames, rotation=60, fontsize=12)
ax.set_xlabel("Learning method")
ax.set_ylabel("Proportion of false path assignments")
build.save_figure(fig,'figures-pif/em_true_paths_percentage')
#fig.savefig("%s/em_true_paths_percentage.pdf"%saving_dir())



''' LL Paths
'''

def get_paths_ll_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                          if key[METRIC_NAME_IDX]=='PATH_LL' \
                          and key[LEARNING_METHOD_IDX]==learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_  in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += [-u for u in vs_]
  return ll_point_by_strat

strategy = 'LAGGED2'
median_vals = []
mean_vals = []
lower_percentile = []
upper_percentile = []
outliers = []
for learning in learning_methods:
    data = get_paths_ll_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    data.sort()
    median_vals.append(data[int(len(data)*0.5)])
    mean_vals.append(np.mean(data))
    lower_percentile.append(data[int(len(data)*0.1)])
    up_idx = int(len(data)*0.9)
    upper_percentile.append(data[up_idx])
    outliers.append(data[up_idx:][::3])


fig = pl.figure(3, figsize=(10,8))
fig.clf()
ax = fig.add_subplot(111)
plt.subplots_adjust(left=0.1, right=0.98, top=0.9, bottom=0.30)
xs = np.arange(num_methods)+1
plot_error_bar(ax, xs, mean_vals, lower_percentile, upper_percentile, fmt='ko')
ax.set_xlim(0.5, num_methods+0.5)
ax.set_ylim(0.0, 25)
ax.set_title("Comparison of the log-likelihoods of the true paths for 1-minute sampling intervals \n (2-lagged smoothing reconstruction)")
ax.set_xticks(xs)
xtickNames = ax.set_xticklabels([learning_display[method_name] for method_name in learning_methods])
plt.setp(xtickNames, rotation=60, fontsize=12)
ax.set_xlabel("Learning method")
ax.set_ylabel("Log-likelihood of true path")
build.save_figure(fig, "figures-pif/em_ll_paths")
#fig.savefig("%s/em_ll_paths.pdf"%saving_dir())


""" NOT USED IN PAPER BEYOND THIS LINE
"""

print "early system exit"
import sys
sys.exit(0)

""" Entropy over paths.
"""

def get_paths_entropy_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                          if key[METRIC_NAME_IDX]=='PATH_ENTROPY' \
                          and key[LEARNING_METHOD_IDX]==learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_  in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += vs_
  return ll_point_by_strat

strategy = 'OFFLINE'
median_vals = []
mean_vals = []
lower_percentile = []
upper_percentile = []
for learning in learning_methods:
    data = get_paths_entropy_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    data.sort()
    median_vals.append(data[int(len(data)*0.5)])
    mean_vals.append(np.mean(data))
    lower_percentile.append(data[int(len(data)*0.05)])
    upper_percentile.append(data[int(len(data)*0.95)])

fig = pl.figure(3)
fig.clf()
ax = fig.gca()
ax.hold(True)
xs = np.arange(num_methods)+1
plot_error_bar(ax, xs, mean_vals, lower_percentile, upper_percentile, fmt='o')
ax.set_xlim(0.5, num_methods+0.5)
ax.set_xticks(xs)
xtickNames = ax.set_xticklabels(learning_methods)
plt.setp(xtickNames, rotation=80, fontsize=12)


''' PATH RELATIVE COVERAGE.
'''

def get_paths_relative_coverage_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                          if key[METRIC_NAME_IDX]=='PATH_RELATIVE_COVERAGE' \
                          and key[LEARNING_METHOD_IDX]==learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_  in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += [1-x for x in vs_]
  return ll_point_by_strat

strategy = 'ONLINE'
median_vals = []
mean_vals = []
lower_percentile = []
upper_percentile = []
for learning in learning_methods:
    data = get_paths_relative_coverage_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    data.sort()
    median_vals.append(data[int(len(data)*0.5)])
    mean_vals.append(np.mean(data))
    lower_percentile.append(data[int(len(data)*0.10)])
    upper_percentile.append(data[int(len(data)*0.88)])

fig = pl.figure(5)
fig.clf()
ax = fig.gca()
ax.hold(True)
xs = np.arange(num_methods)+1
plot_error_bar(ax, xs, median_vals, lower_percentile, upper_percentile, fmt='o')
ax.set_xlim(0.5, num_methods+0.5)
ax.set_xticks(xs)
xtickNames = ax.set_xticklabels(learning_methods)
plt.setp(xtickNames, rotation=80, fontsize=12)

