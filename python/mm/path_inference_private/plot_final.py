import logging

__author__ = 'tjhunter'

'''  
Created on Nov 28, 2011

@author: tjhunter

Plotting script.
PLOT_EXPORT=../papers/2011_PathInference/images/  PYTHONPATH=. MM_DATA_DIR="/home/tjhunter/tmp/high_frequency/" python mm/path_inference_private/plot_final.py
PLOT_EXPORT="/home/tjhunter/work/mm/mm_code/mobilemillennium/arterial/paper/IEEE TITS 2010/figs-gen/"  PYTHONPATH=.  python mm/path_inference_private/plot_final.py 
PLOT_EXPORT="/home/tjhunter/work/mm/mm_code/mobilemillennium/arterial/paper/IEEE TITS 2010/figs-gen/"  ipython -pylab 
PLOT_EXPORT="/home/tjhunter/work/phd-code/papers/2011_PathInference/IEEE TITS 2010/figs-gen/"  ipython -pylab 
'''
# Import all the hacks
import build

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from collections import defaultdict
import cPickle as pickle
from mm.path_inference_private.proj_templates import get_learned_parameter_file
from mm.path_inference_private.evaluation import LEARNING_METHOD_IDX, METRIC_NAME_IDX, STRAT_NAME_IDX
from matplotlib.ticker import MaxNLocator
import random
import math

random.seed = 1
from mm.path_inference_private.plot_utils import *

font_size = 25
figures_width = 10

logging.info("Loading data...")
all_evals = {}
learned_parameters = {}
all_res = [1, 10, 30, 60, 90, 120]
for res in all_res:
  all_evals[res] = get_all_eval(res=res)
  learned_parameters[res] = []
  for batch_idx in range(10):
    try:
      data = pickle.load(get_learned_parameter_file(res=res, batch_idx=batch_idx))
      learned_parameters[res].append(data)
    except IOError:
      pass

colors = {'most_likely_simple': 'red', \
          'em_simple': 'magenta', \
          'most_likely_fancy': 'orange', \
          'em_fancy': 'k', \
          'shortest_path': 'blue', \
          'closest_point': 'green', \
  }
strat_c = {'ONLINE': 'red', 'LAGGED1': 'orange', 'LAGGED2': 'green', 'OFFLINE': 'blue'}
learning_display = {'most_likely_simple': 'MaxLL - simple', \
                    'em_simple': 'EM - simple', \
                    'most_likely_fancy': 'MaxLL - complex', \
                    'em_fancy': 'EM - complex', \
                    'shortest_path': 'Shortest path', \
                    'closest_point': 'Closest point', \
  }

''' TRUE POINTS.
'''

''' First plot: simply the percentage of wrong paths for a given strategy,
with some error bars.
'''

#fig = pl.figure(1)
#ax = fig.gca()
#ys = [percent_wrong(get_true_point_by_strat(all_eval=all_evals[res], learning_method='most_likely_simple')['LAGGED2']) for res in all_res]
#ax.plot(all_res, ys)
#fig.show()

print ">> True points:"
fig = pl.figure(3)
fig.clf()
ax = fig.gca()
ax.hold(True)
strategy = 'VITERBI'
learning_methods = ['em_simple', 'most_likely_simple', 'most_likely_fancy', 'shortest_path', 'closest_point']
num_boot_samples = 100
for learning in learning_methods:
  median_vals = []
  mean_vals = []
  lower_percentile = []
  upper_percentile = []
  for res in all_res:
    data = get_true_point_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    stat_dis = bootstrap_percent_wrong(data, num_boot_samples)
    median_vals.append(stat_dis[int(num_boot_samples * 0.5)])
    mean_vals.append(np.mean(stat_dis))
    lower_percentile.append(stat_dis[int(num_boot_samples * 0.05)])
    upper_percentile.append(stat_dis[int(num_boot_samples * 0.95)])
  #  ax.errorbar(all_res, median_vals, (lower_percentile, upper_percentile), label=learning)
  print learning
  ax.plot(all_res, mean_vals, c=colors[learning], label=learning_display[learning])
  ax.plot(all_res, median_vals, 's', c=colors[learning])
  ax.plot(all_res, lower_percentile, '-.', c=colors[learning])
  ax.plot(all_res, upper_percentile, '-.', c=colors[learning])

strategy = 'ONLINE'
learning_methods = ['closest_point']
num_boot_samples = 100
for learning in learning_methods:
  median_vals = []
  mean_vals = []
  lower_percentile = []
  upper_percentile = []
  for res in all_res:
    data = get_true_point_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    stat_dis = bootstrap_percent_wrong(data, num_boot_samples)
    median_vals.append(stat_dis[int(num_boot_samples * 0.5)])
    mean_vals.append(np.mean(stat_dis))
    lower_percentile.append(stat_dis[int(num_boot_samples * 0.05)])
    upper_percentile.append(stat_dis[int(num_boot_samples * 0.95)])
  c = 'k'
  ax.plot(all_res, mean_vals, c=c, label='Hard closest point')
  ax.plot(all_res, median_vals, 's', c=c)
  ax.plot(all_res, lower_percentile, '-.', c=c)
  ax.plot(all_res, upper_percentile, '-.', c=c)

ax.set_xlabel("Sampling period (seconds)", fontsize=font_size)
ax.set_ylabel("Proportion of false point assignments", fontsize=font_size)
#ax.set_ylim([0,.2])
ax.set_xlim([0, max(all_res) + 10])
ax.set_xticks(all_res)
for tick in ax.xaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

leg = ax.legend(ncol=2, loc=1)
ltext = leg.get_texts()
plt.setp(ltext, fontsize=font_size * .7)
fig.set_size_inches(figures_width, 9)
#fig.show()
logging.info("true_points_percentage")
build.save_figure(fig, "figures-pif/true_points_percentage")
#print "%s/true_points_percentage.pdf" % saving_dir()
#fig.savefig("%s/true_points_percentage.pdf" % saving_dir(), bbox_inches='tight')

''' TRUE PATHS.
'''
fig = pl.figure(3)
fig.clf()
ax = fig.gca()
ax.hold(True)
strategy = 'VITERBI'
learning_methods = ['em_simple', 'most_likely_simple', 'most_likely_fancy', 'shortest_path', 'closest_point']
num_boot_samples = 200
for learning in learning_methods:
  median_vals = []
  mean_vals = []
  lower_percentile = []
  upper_percentile = []
  for res in all_res:
    data = get_true_path_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    stat_dis = bootstrap_percent_wrong(data, num_boot_samples)
    median_vals.append(stat_dis[int(num_boot_samples * 0.5)])
    mean_vals.append(np.mean(stat_dis))
    lower_percentile.append(stat_dis[int(num_boot_samples * 0.05)])
    upper_percentile.append(stat_dis[int(num_boot_samples * 0.95)])
  #  ax.errorbar(all_res, median_vals, (lower_percentile, upper_percentile), label=learning)
  print learning
  ax.plot(all_res, mean_vals, c=colors[learning], label=learning_display[learning])
  ax.plot(all_res, median_vals, 's', c=colors[learning])
  ax.plot(all_res, lower_percentile, '-.', c=colors[learning])
  ax.plot(all_res, upper_percentile, '-.', c=colors[learning])

# Add the plot corresponding to closest point / hard
strategy = 'ONLINE'
learning_methods = ['closest_point']
num_boot_samples = 200
for learning in learning_methods:
  median_vals = []
  mean_vals = []
  lower_percentile = []
  upper_percentile = []
  for res in all_res:
    data = get_true_path_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
    stat_dis = bootstrap_percent_wrong(data, num_boot_samples)
    median_vals.append(stat_dis[int(num_boot_samples * 0.5)])
    mean_vals.append(np.mean(stat_dis))
    lower_percentile.append(stat_dis[int(num_boot_samples * 0.05)])
    upper_percentile.append(stat_dis[int(num_boot_samples * 0.95)])
  c = 'k'
  ax.plot(all_res, mean_vals, c=c, label='Hard closest point')
  ax.plot(all_res, median_vals, 's', c=c)
  ax.plot(all_res, lower_percentile, '-.', c=c)
  ax.plot(all_res, upper_percentile, '-.', c=c)

ax.set_ylabel("Proportion of false path assignments", fontsize=font_size)
ax.set_xlabel("Sampling period (seconds)", fontsize=font_size)
ax.set_xticks(all_res)
ax.set_xlim([0, max(all_res) + 10])
#ax.legend(bbox_to_anchor=(0., -0., 1, 0.1), loc=4, \
#       ncol=2, borderaxespad=0.)
fig.set_size_inches(figures_width, 9)
# Size adjutments
for tick in ax.xaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

leg = ax.legend(ncol=2, loc=1)
ltext = leg.get_texts()
plt.setp(ltext, fontsize=font_size * .7)
#fig.show()
logging.info("true_paths_percentage")
build.save_figure(fig, "figures-pif/true_paths_percentage")
#fig.savefig("%s/true_paths_percentage.pdf" % saving_dir(), bbox_inches='tight')




# True points, complex strategy:
def get_points_ll_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                        if key[METRIC_NAME_IDX] == 'POINT_LL' \
      and key[LEARNING_METHOD_IDX] == learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_ in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += vs_
  return ll_point_by_strat


''' LL Paths
'''
ll_paths_font_size = 15


def get_paths_ll_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                        if key[METRIC_NAME_IDX] == 'PATH_LL' \
      and key[LEARNING_METHOD_IDX] == learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_ in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += [-u for u in vs_]
  return ll_point_by_strat


fig = pl.figure(3)
fig.clf()
strategies = ['ONLINE', 'LAGGED1', 'LAGGED2', 'OFFLINE']
learning_methods = ['most_likely_simple', 'most_likely_fancy', 'em_simple']
max_vals_plot = [10, 10, 100]
for learning_idx in range(len(learning_methods)):
  learning = learning_methods[learning_idx]
  ax = fig.add_subplot(len(learning_methods), 1, learning_idx + 1)
  for strategy in strategies:
    median_vals = []
    mean_vals = []
    lower_percentile = []
    upper_percentile = []
    for res in all_res:
      data = get_paths_ll_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
      data.sort()
      median_vals.append(data[int(len(data) * 0.5)])
      mean_vals.append(np.mean(data))
      lower_percentile.append(data[int(len(data) * 0.25)])
      upper_percentile.append(data[int(len(data) * 0.75)])
    ax.plot(all_res, median_vals, c=strat_c[strategy], label="%s" % (strategy))
    ax.plot(all_res, mean_vals, 's', c=strat_c[strategy])
    ax.plot(all_res, lower_percentile, '-.', c=strat_c[strategy])
    ax.plot(all_res, upper_percentile, '-.', c=strat_c[strategy])
  ax.set_ylabel("Log-likelihood \nof true paths\n%s" % learning_display[learning], multialignment='center',
                fontsize=ll_paths_font_size)
  ax.set_xticks([])
  ax.set_ylim([0, max_vals_plot[learning_idx]])
  ax.set_xlim([0, max(all_res)])
  # Size adjutments
  ax.yaxis.set_major_locator(MaxNLocator(5))
  for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(ll_paths_font_size)
  for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(ll_paths_font_size)

  # Add a lagend for the last one:
ax.set_xlabel("Sampling period (seconds)", fontsize=ll_paths_font_size)
ax.set_xticks(all_res)
leg = ax.legend(bbox_to_anchor=(0., -0.5, 1, 0.1), loc=3, \
                ncol=4, mode="expand", borderaxespad=1.)
fig.set_size_inches(figures_width, 9)
#fig.show()
logging.info("ll_paths")
build.save_figure(fig, "figures-pif/ll_paths")
#fig.savefig("%s/ll_paths.pdf" % (saving_dir()),
#            bbox_inches=mpl.transforms.Bbox.from_bounds(0, 0, figures_width - .6, 8.4))

""" Entropy over paths.
"""
entropy_path_font_size = 15


def get_paths_entropy_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                        if key[METRIC_NAME_IDX] == 'PATH_ENTROPY' \
      and key[LEARNING_METHOD_IDX] == learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_ in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += vs_
  return ll_point_by_strat


fig = pl.figure(3)
fig.clf()
strategies = ['ONLINE', 'LAGGED1', 'LAGGED2', 'OFFLINE']
learning_methods = ['most_likely_simple', 'most_likely_fancy', 'em_simple']
for learning_idx in range(len(learning_methods)):
  learning = learning_methods[learning_idx]
  ax = fig.add_subplot(len(learning_methods), 1, learning_idx + 1)
  for strategy in strategies:
    median_vals = []
    mean_vals = []
    lower_percentile = []
    upper_percentile = []
    for res in all_res:
      data = get_paths_entropy_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
      data.sort()
      median_vals.append(data[int(len(data) * 0.5)])
      mean_vals.append(np.mean(data))
      lower_percentile.append(data[int(len(data) * 0.05)])
      upper_percentile.append(data[int(len(data) * 0.95)])
    ax.plot(all_res, median_vals, c=strat_c[strategy], label="%s" % (strategy))
    ax.plot(all_res, mean_vals, 's', c=strat_c[strategy])
    ax.plot(all_res, lower_percentile, '-.', c=strat_c[strategy])
    ax.plot(all_res, upper_percentile, '-.', c=strat_c[strategy])
  ax.set_ylabel("Entropy of paths\n(%s)" % learning_display[learning], multialignment='center',
                fontsize=entropy_path_font_size)
  ax.set_xticks([])
  ax.set_xlim([0, max(all_res) + 5])
  # Size adjutments
  ax.yaxis.set_major_locator(MaxNLocator(5))
  for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(entropy_path_font_size)
  for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(entropy_path_font_size)

  # Add a lagend for the last one:
ax.set_xlabel("Sampling period (seconds)", fontsize=entropy_path_font_size)
ax.set_xticks(all_res)
ax.legend(bbox_to_anchor=(0., -0.5, 1, 0.1), loc=3, \
          ncol=4, mode="expand", borderaxespad=1.)
fig.set_size_inches(figures_width, 9)
#fig.show()
logging.info("entropy_paths")
build.save_figure(fig, "figures-pif/entropy_paths")
#fig.savefig("%s/entropy_paths.pdf" % (saving_dir()),
#            bbox_inches=mpl.transforms.Bbox.from_bounds(0, 0, figures_width - .5, 8.5))

''' ENTROPY POINTS.
'''
entropy_point_font_size = 15


def get_points_entropy_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                        if key[METRIC_NAME_IDX] == 'POINT_ENTROPY' \
      and key[LEARNING_METHOD_IDX] == learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_ in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += vs_
  return ll_point_by_strat


fig = pl.figure(3)
fig.clf()
strategies = ['ONLINE', 'LAGGED1', 'LAGGED2', 'OFFLINE']
learning_methods = ['most_likely_simple', 'most_likely_fancy', 'em_simple']
for learning_idx in range(len(learning_methods)):
  learning = learning_methods[learning_idx]
  ax = fig.add_subplot(len(learning_methods), 1, learning_idx + 1)
  for strategy in strategies:
    median_vals = []
    mean_vals = []
    lower_percentile = []
    upper_percentile = []
    for res in all_res:
      data = get_points_entropy_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
      data.sort()
      median_vals.append(data[int(len(data) * 0.5)])
      mean_vals.append(np.mean(data))
      lower_percentile.append(data[int(len(data) * 0.05)])
      upper_percentile.append(data[int(len(data) * 0.95)])
    ax.plot(all_res, median_vals, c=strat_c[strategy], label="%s" % (strategy))
    ax.plot(all_res, mean_vals, 's', c=strat_c[strategy])
    ax.plot(all_res, lower_percentile, '-.', c=strat_c[strategy])
    ax.plot(all_res, upper_percentile, '-.', c=strat_c[strategy])
  ax.set_ylabel("Entropy of points\n(%s)" % learning_display[learning], multialignment='center',
                fontsize=entropy_point_font_size)
  ax.set_xticks([])
  ax.set_xlim([0, max(all_res) + 10])
  # Size adjutments
  ax.yaxis.set_major_locator(MaxNLocator(5))
  for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(entropy_point_font_size)
  for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(entropy_point_font_size)

  # Add a lagend for the last one:
ax.set_xlabel("Sampling period (seconds)", fontsize=entropy_point_font_size)
ax.set_xticks(all_res)
ax.legend(bbox_to_anchor=(0., -0.5, 1, 0.1), loc=3, \
          ncol=4, mode="expand", borderaxespad=1.)
fig.set_size_inches(figures_width, 9)
# Size adjutments
for tick in ax.xaxis.get_major_ticks():
  tick.label.set_fontsize(entropy_point_font_size)

for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(entropy_point_font_size)

leg = ax.legend(ncol=2, loc=1)
ltext = leg.get_texts()
plt.setp(ltext, fontsize=entropy_point_font_size)
#fig.show()
logging.info("entropy_points")
build.save_figure(fig, "figures-pif/entropy_points")
#fig.savefig("%s/entropy_points.pdf" % (saving_dir()),
#            bbox_inches=mpl.transforms.Bbox.from_bounds(0, 0, figures_width - .5, 8.5))

''' PATH COVERAGE
'''
coverage_font_size = 15


def get_paths_coverage_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                        if key[METRIC_NAME_IDX] == 'PATH_COVERAGE' \
      and key[LEARNING_METHOD_IDX] == learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_ in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += vs_
  return ll_point_by_strat


fig = pl.figure(3)
fig.clf()
strategies = ['ONLINE', 'LAGGED1', 'LAGGED2', 'OFFLINE']
learning_methods = ['most_likely_simple', 'most_likely_fancy', 'em_simple']
for learning_idx in range(len(learning_methods)):
  learning = learning_methods[learning_idx]
  ax = fig.add_subplot(len(learning_methods), 1, learning_idx + 1)
  for strategy in strategies:
    median_vals = []
    mean_vals = []
    lower_percentile = []
    upper_percentile = []
    for res in all_res:
      data = get_paths_coverage_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
      data.sort()
      median_vals.append(data[int(len(data) * 0.5)])
      mean_vals.append(np.mean(data))
      lower_percentile.append(data[int(len(data) * 0.10)])
      upper_percentile.append(data[int(len(data) * 0.90)])
    ax.plot(all_res, median_vals, c=strat_c[strategy], label="%s" % (strategy))
    ax.plot(all_res, mean_vals, 's', c=strat_c[strategy])
    ax.plot(all_res, lower_percentile, '-.', c=strat_c[strategy])
    ax.plot(all_res, upper_percentile, '-.', c=strat_c[strategy])
  ax.set_ylabel("Path coverage (m)\n%s" % learning_display[learning], multialignment='center',
                fontsize=coverage_font_size)
  ax.set_xlim([0, max(all_res) + 10])
  # Size adjutments
  ax.yaxis.set_major_locator(MaxNLocator(5))
  for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(coverage_font_size)
  for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(coverage_font_size)

  # Add a lagend for the last one:
ax.set_xlabel("Sampling period (seconds)", fontsize=coverage_font_size)
ax.set_xticks(all_res)
ax.legend(bbox_to_anchor=(0., -0.5, 1, 0.1), loc=3, \
          ncol=4, mode="expand", borderaxespad=1.)
fig.set_size_inches(figures_width, 9)

leg = ax.legend(ncol=2, loc=1)
ltext = leg.get_texts()
plt.setp(ltext, fontsize=coverage_font_size)
#fig.show()
logging.info("coverage_paths")
build.save_figure(fig, "figures-pif/coverage_paths")
#fig.savefig("%s/coverage_paths.pdf" % (saving_dir()),
#            bbox_inches=mpl.transforms.Bbox.from_bounds(0, 0, figures_width - .5, 8.5))

''' PATH RELATIVE COVERAGE.
'''


def get_paths_relative_coverage_by_strat(all_eval, learning_method):
  ll_point_data = dict([(key, all_eval[key]) for key in all_eval \
                        if key[METRIC_NAME_IDX] == 'PATH_RELATIVE_COVERAGE' \
      and key[LEARNING_METHOD_IDX] == learning_method])
  ll_point_by_strat = defaultdict(list)
  for key, vals in ll_point_data.iteritems():
    for vs in vals:
      for vs_ in vs:
        ll_point_by_strat[key[STRAT_NAME_IDX]] += [1 - x for x in vs_]
  return ll_point_by_strat


relative_coverage_font_size = 15
fig = pl.figure(3)
fig.clf()
strategies = ['ONLINE', 'LAGGED1', 'LAGGED2', 'OFFLINE']
learning_methods = ['most_likely_simple', 'most_likely_fancy', 'em_simple']
for learning_idx in range(len(learning_methods)):
  learning = learning_methods[learning_idx]
  ax = fig.add_subplot(len(learning_methods), 1, learning_idx + 1)
  for strategy in strategies:
    median_vals = []
    mean_vals = []
    lower_percentile = []
    upper_percentile = []
    for res in all_res:
      data = get_paths_relative_coverage_by_strat(all_eval=all_evals[res], learning_method=learning)[strategy]
      data.sort()
      median_vals.append(data[int(len(data) * 0.5)])
      mean_vals.append(np.mean(data))
      lower_percentile.append(data[int(len(data) * 0.20)])
      upper_percentile.append(data[int(len(data) * 0.80)])
    ax.plot(all_res, median_vals, c=strat_c[strategy], label="%s" % (strategy))
    ax.plot(all_res, mean_vals, 's', c=strat_c[strategy])
    ax.plot(all_res, lower_percentile, '-.', c=strat_c[strategy])
    ax.plot(all_res, upper_percentile, '-.', c=strat_c[strategy])
  ax.set_ylabel("Relative coverage\n(%s)" % learning_display[learning], multialignment='center',
                fontsize=relative_coverage_font_size)
  ax.set_ylim([0, 1])
  ax.set_xticks([])
  ax.set_xlim([0, max(all_res) + 10])
  for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(relative_coverage_font_size)
  for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(relative_coverage_font_size)

  # Add a lagend for the last one:
ax.set_xlabel("Sampling period (seconds)")
ax.set_xticks(all_res)
ax.legend(bbox_to_anchor=(0., -0.5, 1, 0.1), loc=3, \
          ncol=4, mode="expand", borderaxespad=1.)
fig.set_size_inches(figures_width, 9)
# Size adjustments
for tick in ax.xaxis.get_major_ticks():
  tick.label.set_fontsize(relative_coverage_font_size)

for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(relative_coverage_font_size)

leg = ax.legend(ncol=2, loc=1)
ltext = leg.get_texts()
plt.setp(ltext, fontsize=relative_coverage_font_size)
#fig.show()
#fig.savefig("%s/relative_coverage_paths.pdf"%(saving_dir()))
logging.info("relative_coverage_paths")
build.save_figure(fig, "figures-pif/relative_coverage_paths")
#fig.savefig("%s/relative_coverage_paths.pdf" % (saving_dir()),
#            bbox_inches=mpl.transforms.Bbox.from_bounds(0, 0, figures_width - .5, 8.5))

''' Analysis of parameters
'''

carac_length_distr = []
mean = []
dev_upper = []
dev_lower = []
for res in all_res:
  data = [-1 / v['most_likely_simple'][0] for v in learned_parameters[res]]
  data.sort()
  carac_length_distr.append(data)
  mean.append(np.mean(data))
  dev_lower.append(-data[int(len(data) * 0)] + np.mean(data))
  dev_upper.append(data[int(len(data) * 0.99)] - np.mean(data))

font_size_ = int(.8 * font_size)
fig = pl.figure(3)
fig.clf()
ax = fig.gca()
ax.errorbar(all_res, mean, [dev_lower, dev_upper], c='k')
ax.set_yscale('log')
ax.set_xlim([0, max(all_res) + 10])
#ax.set_xlabel("Sampling period (seconds)", fontsize=font_size_)
ax.set_ylabel("Learned proper length (m)", fontsize=font_size_)
ax.set_xticks(all_res)
fig.set_size_inches(figures_width, 5)
# Size adjutments
for tick in ax.xaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

# There is a bug somewhere in mpl, need to use png
logging.info("proper_length")
build.save_figure(fig, "figures-pif/proper_length")
#fig.savefig("%s/proper_length.png" % (saving_dir()), dpi=300)

fig = pl.figure(3)
fig.clf()
ax = fig.gca()

std_dev_distr = []
mean = []
dev_upper = []
dev_lower = []
for res in all_res:
  data = [1 / math.sqrt(v['most_likely_simple'][-1]) for v in learned_parameters[res]]
  data.sort()
  print data
  std_dev_distr.append(data)
  mean.append(np.mean(data))
  dev_lower.append(-data[int(len(data) * 0.0)] + np.mean(data))
  dev_upper.append(data[int(len(data) * 0.99)] - np.mean(data))

ax.errorbar(all_res, mean, [dev_lower, dev_upper], c='k')

mean = []
dev_upper = []
dev_lower = []
for res in all_res:
  data = [1 / math.sqrt(v['em_simple'][-1]) for v in learned_parameters[res]]
  data.sort()
  print data
  mean.append(np.mean(data))
  dev_lower.append(-data[int(len(data) * 0.0)] + np.mean(data))
  dev_upper.append(data[int(len(data) * 0.99)] - np.mean(data))

ax.errorbar(all_res, mean, [dev_lower, dev_upper], c='r')

font_size_ = int(.8 * font_size)
ax.set_xlim([0, max(all_res) + 10])
#ax.set_xlabel("Sampling period (seconds)", fontsize=font_size)
ax.set_ylabel("Learned standard deviation (m)", fontsize=font_size_)
ax.set_xticks(all_res)
ax.set_ylim([0, 9])
ax.yaxis.set_major_locator(MaxNLocator(5))
# Size adjutments
for tick in ax.xaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

#fig.show()
fig.set_size_inches(figures_width, 5)
logging.info("proper_std_dev")
build.save_figure(fig, "figures-pif/proper_std_dev")
#fig.savefig("%s/proper_std_dev.pdf" % (saving_dir()))

fig = pl.figure(3)
fig.clf()
ax = fig.gca()

left_turn_distr = []
mean = []
dev_upper = []
dev_lower = []
for res in all_res:
  data = [v['most_likely_fancy'][3] for v in learned_parameters[res]]
  data.sort()
  left_turn_distr.append(data)
  mean.append(np.mean(data))
  dev_lower.append(-data[int(len(data) * 0.0)] + np.mean(data))
  dev_upper.append(data[int(len(data) * 0.99)] - np.mean(data))

ax.errorbar(all_res, mean, [dev_lower, dev_upper], c='b', label="Right")

right_turn_distr = []
mean = []
dev_upper = []
dev_lower = []
for res in all_res:
  data = [v['most_likely_fancy'][4] for v in learned_parameters[res]]
  data.sort()
  right_turn_distr.append(data)
  mean.append(np.mean(data))
  dev_lower.append(-data[int(len(data) * 0.0)] + np.mean(data))
  dev_upper.append(data[int(len(data) * 0.99)] - np.mean(data))

ax.errorbar(all_res, mean, [dev_lower, dev_upper], c='g', label="Left")
ax.plot(all_res, [0 for _ in all_res], c='k')
ax.set_xlim([2, max(all_res) + 10])
#ax.set_xlabel("Sampling period (seconds)")
ax.set_ylabel("Weight", fontsize=font_size)
ax.set_xticks(all_res)
ax.set_ylim([-1, 1])
# Matplotlib 1.2.0 has a bug in the font system, so that the minus sign is incorrectly rendered.
# Manually creating the ticks as a workaround.
yts = ax.get_yticks()
ax.set_yticklabels([str(yt) for yt in yts])
leg = ax.legend()
# Size adjutments
for tick in ax.xaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

for tick in ax.yaxis.get_major_ticks():
  tick.label.set_fontsize(font_size)

#leg = ax.legend(ncol=2, loc=1)
ltext = leg.get_texts()
plt.setp(ltext, fontsize=font_size)
#fig.show()
fig.set_size_inches(figures_width, 5)
logging.info("left_right")
build.save_figure(fig, "figures-pif/left_right")
#fig.savefig("%s/left_right.pdf" % (saving_dir()))

