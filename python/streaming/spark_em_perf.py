'''
Created on Nov 27, 2012

@author: tjhunter
'''
import build
import numpy as np
import matplotlib.pyplot as plt

# Maybe to do one day...
ec2_data = """ c20   20   0.013000   0.150000   1915.281006   0.015000   1.805000   801.680015   0.071000   363.179991   2.024000   748.418006   9.950000   0.383000   0.017000   
c40   30   0.028000   0.135000   1282.974000   0.018000   2.241000   635.114998   0.080000   206.913994   2.585000   438.500996   11.704000   0.507000   0.019000   
c80   40   0.021000   0.140000   1201.686997   0.016000   2.237000   639.044004   0.085000   188.172999   4.141000   372.034004   11.473000   0.416000   0.018000   
test_10am   10   0.020000   0.122000   4499.750031   0.016000   2.292000   2288.681962   0.097000   653.513996   2.710000   1555.192000   16.250999   0.401000   0.017000 """

nersc_data = """nersc160   50   0.012000   0.096000   263.585000   0.012000   0.136000   123.206000   0.096000   50.712000   0.843000   89.400000   48.608002   1.239000   0.011000   
nersc80   40   0.015000   0.091000   386.947995   0.012000   0.072000   137.154000   0.083000   93.370000   0.679000   156.222999   91.190002   1.135000   0.011000   
nersc4   10   0.015000   0.104000   4658.411042   0.017000   0.104000   1075.220994   0.080000   1361.113007   0.721000   2221.821028   60.931000   0.353000   0.014000   
nersc20   20   0.124000   4.463000   1244.278999   2.346000   0.094000   350.896998   0.060000   320.513000   0.592000   563.044004   95.424004   5.433000   1.440000   
nersc40   30   0.014000   0.086000   734.162003   0.012000   0.104000   217.355002   0.087000   177.391998   0.649000   339.183003   60.335999   1.850000   0.012000   """
labels = "expt_id   num_slaves   samples_postflatten   post_mstep   em   samples_preflatten   broadcast   mstep   loadData   ll_compute   InitializeSpark   samples_groupby   initialize   output   sampling   "

def process_line(s):
  toks = s.split()
  num_cores = int(toks[1])
  em = float(toks[4])
  mstep = float(toks[7])
  ll_compute = float(toks[9])
  samples_groupby = float(toks[11])
  init = float(toks[12])
  return (num_cores, mstep, ll_compute, samples_groupby)
  
  

ec2_clean_data = sorted([process_line(s) for s in ec2_data.split('\n')], key=lambda tup: tup[0])
nersc_clean_data = sorted([process_line(s) for s in nersc_data.split('\n')], key=lambda tup: tup[0])



def makefig(data, figindex, ytop, xlabel=None):
  width = 4.0 
  ind = np.array([num_cores for (num_cores, _, _, _) in data])
  m = np.array([mstep for (_, mstep, _, _) in data])
  e = np.array([ll_compute for (_, _, ll_compute, _) in data])
  gb = np.array([samples_groupby for (_, _, _, samples_groupby) in data])
  fig = plt.figure(figindex, figsize=(4,2))
  ax = fig.gca()
  ax.bar(ind, m, width, color='k', label="M step")
  ax.bar(ind, gb, width, bottom=m, color='grey', label="Shuffle")
  ax.bar(ind, e, width, bottom=m + gb, color='white', label='E step')
  ax.set_ylabel('Iteration time (sec)')
  ax.set_xticks(ind + width / 2.)
  ax.set_yticks([0,2000,4000])
  ax.set_xticklabels([str(i) for i in ind])
  ax.set_xlim(min(ind)-2, max(ind)+6)
  ax.set_ylim(top=ytop)
  if xlabel:
    ax.legend(prop={'size':11})
    ax.set_xlabel(xlabel)
  return fig

fig = makefig(ec2_clean_data, 0, 4800, "Number of nodes")
build.save_figure(fig, "figures-socc/spark_em_perf_ec2")
#fig.savefig('%s/spark_em_perf_ec2.pdf' % (defs.save_path()), bbox_inches='tight')

fig = makefig(nersc_clean_data, 1, 4800)
build.save_figure(fig, "figures-socc/spark_em_perf_nersc")
#fig.savefig('%s/spark_em_perf_nersc.pdf' % (defs.save_path()), bbox_inches='tight')

