'''
Created on Nov 6, 2012

@author: tjhunter
'''
import build
from mm.data.codec_json import decode_RouteTT
import json
import numpy as np
import scipy.stats as sstats
import logging

class ErrorStatistics(object):
  def __init__(self, tt_mean, tt_std_dev, tt_obs, log_pdf, percentile):
    self.ttMean = tt_mean
    self.ttStdDev = tt_std_dev
    self.ttObs = tt_obs
    self.logPdf = log_pdf
    self.percentile = percentile

class TestResult(object):
  def __init__(self, routeTT, stat):
    self.routeTT = routeTT
    self.stat = stat

def decode_ErrorStatistics(dct):
  tt_mean = float(dct['ttMean'])
  tt_std_dev = float(dct['ttStdDev'])
  tt_obs = float(dct['ttObs'])
  log_pdf = float(dct['logPdf'])
  percentile = float(dct['percentile'])
  return ErrorStatistics(tt_mean, tt_std_dev, tt_obs, log_pdf, percentile)

def decode_TestResult(dct):
  routeTT = decode_RouteTT(dct['routeTT'])
  stat = decode_ErrorStatistics(dct['stat'])
  return TestResult(routeTT, stat)

def L1(stats):
  dt = np.abs(np.array([(stat.ttMean - stat.ttObs) for stat in stats]))
  m_score = np.mean(dt)
  up_score = sstats.scoreatpercentile(dt, 93)
  low_score = sstats.scoreatpercentile(dt, 7)
  return (low_score, m_score, up_score)

def L2(stats):
  dt = (np.array([(stat.ttMean - stat.ttObs) for stat in stats])) ** 2
  m_score = np.sqrt(np.mean(dt))
  up_score = np.sqrt(sstats.scoreatpercentile(dt, 93))
  low_score = np.sqrt(sstats.scoreatpercentile(dt, 7))
  return (low_score, m_score, up_score)

def readExperiment(experiment, interval, num_reads=100):
  f = open(build.data_name("tase/perf/%s/%s.txt"%(experiment,interval)),'r')
  results = []
  for l in f:
    dct = json.loads(l)
    tr = decode_TestResult(dct)
    results.append(tr)
    if len(results) > num_reads:
      break
  return results

experiments = ["SlidingBig", "SlidingBig1", "SlidingBig2", "SlidingBig3", "SlidingBig4"]
intervals = ['PT50S', 'PT230S', 'PT650S', 'PT1250S']
interval_times = np.array([50.0, 230.0, 650.0, 1250.0])
labels = ['1', '5', '10', '20']
#path_SlidingBig = "/windows/D/arterial_experiments/tase/perf/"

experiment = experiments[0]
interval = intervals[3]
#f = open('%s/%s/%s.txt'%(path_SlidingBig, experiment, interval))
#results = []
#for l in f:
#  dct = json.loads(l)
#  tr = decode_TestResult(dct)
#  results.append(tr)
#  if len(results) > 1000:
#    break
import pylab as pl


#dt = np.array([(stat.ttMean - stat.ttObs) for stat in stats])
#
#means = [(stat.ttMean - stat.ttObs)/stat.ttMean for stat in stats]
#
#means = [(stat.ttMean) for stat in stats]
#
#lls = [stat.logPdf for stat in stats]
#percentiles = [stat.percentile for stat in stats]

if __name__ == '__main__':
  logging.info("Running LL plots")
  lls_by_exp = {}
  for experiment in experiments:
    ms = []
    ups = []
    lows = []
    for interval in intervals:
      results = readExperiment(experiment, interval)
      stats = [tr.stat for tr in results]
      lls = np.array([stat.logPdf for stat in stats])
      m_score = np.median(lls)
      up_score = sstats.scoreatpercentile(lls, 90)
      low_score = sstats.scoreatpercentile(lls, 10)
      ms.append(m_score)
      ups.append(up_score)
      lows.append(low_score)
    
    ms = np.array(ms)
    ups = np.array(ups)
    lows = np.array(lows)
    lls_by_exp[experiment] = ms
  
  
  fig = pl.figure(figsize=(4, 3))
  ax = fig.gca()
  plot_names = []
  lls_by_exp_names = sorted(lls_by_exp.keys())
  for lls_by_exp_name in lls_by_exp_names:
    means = lls_by_exp[lls_by_exp_name]
    ax.plot(means, label=lls_by_exp_name)
  
  ax.set_xlabel("Travel time interval (min)")
  ax.set_ylabel("Meadian log-likelihood")
  ax.set_xticks(range(len(interval_times)))
  ax.set_xticklabels(labels)
  leg = ax.legend(loc="lower left",prop={'size':11})
#  fig.show()
  build.save_figure(fig, "figures-socc/ll_%s"%experiment)
#  fig.savefig('%s/ll_%s.pdf' % (defs.save_path(), experiment), bbox_inches='tight')
    
  print "Running L1/L2 plots"
  plot_size = (3,2)
  for experiment in experiments:
    l1_downs = []
    l1_means = []
    l1_ups = []
    l2_downs = []
    l2_means = []
    l2_ups = []
    print "experiment: " + experiment
    
    for interval in intervals:
      results = readExperiment(experiment, interval)
      stats = [tr.stat for tr in results]
      (l1_down, l1_mean, l1_up) = L1(stats)
      (l2_down, l2_mean, l2_up) = L2(stats)
      l1_downs.append(l1_down)
      l1_ups.append(l1_up)
      l1_means.append(l1_mean)  
      l2_downs.append(l2_down)
      l2_ups.append(l2_up)
      l2_means.append(l2_mean) 
    
    l1_downs = np.array(l1_downs)
    l1_means = np.array(l1_means)
    l1_ups = np.array(l1_ups)
    
    
    fig = pl.figure(figsize=plot_size)
    ax = fig.gca()
    ax.plot(l1_downs / interval_times, 'k--')
    ax.plot(l1_means / interval_times, 'ko-')
    ax.plot(l1_ups / interval_times, 'k--')
    ax.set_ylim(0,4.0)
    ax.set_yticks([0,1,2,3,4])
    ax.set_xlabel("Travel time interval (min)")
    ax.set_ylabel("Relative mean absolute deviation")
    ax.set_xticks(range(len(interval_times)))
    ax.set_xticklabels(labels)
    ax.text(0.4, 0.8, experiment, transform = ax.transAxes)
    build.save_figure(fig, "figures-socc/rl1_%s"%experiment)
#    fig.show()
#    fig.savefig('%s/rl1_%s.pdf' % (defs.save_path(), experiment), bbox_inches='tight')
    
    fig = pl.figure(figsize=plot_size)
    ax = fig.gca()
    ax.plot(l2_downs / interval_times, 'k--')
    ax.plot(l2_means / interval_times, 'ko-')
    ax.plot(l2_ups / interval_times, 'k--')
    ax.set_ylim(0,4.0)
    ax.set_yticks([0,1,2,3,4])
    ax.set_xlabel("Travel time interval (min)")
    ax.set_ylabel("Relative RMSE")
    ax.set_xticks(range(len(interval_times)))
    ax.set_xticklabels(labels)
    ax.text(0.4, 0.8, experiment, transform = ax.transAxes)
    build.save_figure(fig, "figures-socc/rl2_%s"%experiment)
#    fig.show()
#    fig.savefig('%s/rl2_%s.pdf' % (defs.save_path(), experiment), bbox_inches='tight')
