__author__ = 'tjhunter'


'''
Created on Jan 22, 2012

@author: tjhunter
'''

import os
from collections import defaultdict
from mm.path_inference_private.proj_templates import get_evaluation_fnames,\
  get_evaluation_data_file
import pickle
from mm.path_inference_private.evaluation import METRIC_NAME_IDX, LEARNING_METHOD_IDX,\
  STRAT_NAME_IDX
import random
import math
random.seed = 1
import numpy as np

def plot_error_bar(ax, xs, ys, lower_percentile, upper_percentile, outliers=None, **kwargs):
  upper = np.array(upper_percentile) - np.array(ys)
  lower = np.array(ys) - np.array(lower_percentile)
  ax.errorbar(xs, ys, yerr=[lower, upper], **kwargs)
  if outliers is not None:
    min_pts = min([len(u) for u in outliers])
    if min_pts < 2:
      return
    n = len(xs)
    for i in range(n):
      this_outliers = outliers[i]
      random.shuffle(this_outliers)
      this_outliers = this_outliers[:min_pts]
      ax.plot([xs[i] for _ in this_outliers], this_outliers, 'b+')


''' LOADING '''


def get_all_eval(res):
  all_eval = defaultdict(list)
  for (_, _res, _batch_idx) in get_evaluation_fnames(res=res):
    fin = get_evaluation_data_file(res=_res, batch_idx=_batch_idx)
    data = pickle.load(fin)
    fin.close()
    for (key, val) in data.iteritems():
      all_eval[key].append(val)
  return all_eval

''' TRUE POINTS.
'''

def percent_wrong(true_point_data):
  good = 0.0
  bad = 0.0
  for (g,b) in true_point_data:
    good += g
    bad += b
  return bad / (bad + good)

def get_true_point_by_strat(all_eval, learning_method):
  true_point_data = dict([(key, all_eval[key]) for key in all_eval \
                          if key[METRIC_NAME_IDX]=='POINT_TRUE' \
                          and key[LEARNING_METHOD_IDX]==learning_method])
#
#  true_point_strategies = set([key[STRAT_NAME_IDX] for key in true_point_data])
  true_point_by_strat = defaultdict(list)
  for key, vals in true_point_data.iteritems():
    for vs in vals:
      true_point_by_strat[key[STRAT_NAME_IDX]] += vs
  return true_point_by_strat

def subsample(data):
  n = len(data)
  assert n
  return [data[random.randint(0,n-1)] for _ in range(n)]

def bootstrap_percent_wrong(true_point_data, num_points):
  res = [percent_wrong(subsample(true_point_data)) for _ in range(num_points)]
  assert res
  res.sort()
  return res

''' TRUE PATHS '''

def get_true_path_by_strat(all_eval, learning_method):
  true_path_data = dict([(key, all_eval[key]) for key in all_eval \
                          if key[METRIC_NAME_IDX]=='PATH_TRUE' \
                          and key[LEARNING_METHOD_IDX]==learning_method])
  true_path_by_strat = defaultdict(list)
  for key, vals in true_path_data.iteritems():
    for vs in vals:
      true_path_by_strat[key[STRAT_NAME_IDX]] += vs
  return true_path_by_strat

