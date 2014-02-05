import logging
from build import data_path

__author__ = 'tjhunter'
'''
Created on Sep 23, 2011

@author: tjhunter


'''
import os
import re
# pylint: disable=W0402
from string import Template
import gzip
import logging
import simplejson as json

def get_data_dir():
  if 'DATA_DIR' in os.environ:
    s = os.environ['DATA_DIR']
    return "%s/path_inference/" % s
  else:
    return "%s/path_inference/"%data_path()
  #return "/windows/D/arterial_data/high_frequency/"

#data_dir = "/windows/D/arterial_data/high_frequency/"
#data_dir = "/mnt2/data/"
# Main data file - used by Jython
data_file = "raw/raw_arterial_201.json.gz"
raw_data_tpl = "projected_id${driver_id}_0of0.json.gz"
_raw_data_tpl_re = "projected_id(.+)_0of0.json.gz"
# Raw tracks - removed all spurious points and split by driver:
raw_tracks_tpl = "raw_points_id${driver_id}.json.gz"
_raw_tracks_tpl_re = "raw_points_id(.+).json.gz"
# The mapped points
mapped_points_tpl = "mapped_points_id${driver_id}.json.gz"
_mapped_points_tpl_re = "mapped_points_id(.+).json.gz"

# The complete mapped tracks
mapped_tracks_tpl = "mapped_tracks_id${driver_id}.json.gz"
_mapped_tracks_tpl_re = "mapped_tracks_id(.+).json.gz"

mapped_trajs_tpl = "mapped_trajs_id${driver_id}_traj${track_idx}_dt${res}.json.gz"
_mapped_trajs_tpl_re = "mapped_trajs_id(.+)_traj([0-9]*)_dt([0-9]*).json.gz"

traj_points_tpl = "traj_points_id${driver_id}_traj${track_idx}_dt${res}.json.gz"
_traj_points_tpl_re = "traj_points_id(.+)_traj([0-9]*)_dt([0-9]*).json.gz"

features_tpl = "features_id${driver_id}_traj${track_idx}_dt${res}.pkl.gz"
features_tpl_re = "features_id(.+)_traj([0-9]*)_dt([0-9]*).pkl.gz"

most_likely_indexes_tpl = "most_likely_indexes_id${driver_id}_traj${track_idx}_dt${res}.pkl"
most_likely_indexes_tpl_re = "most_likely_indexes_id(.+)_traj([0-9]*)_dt([0-9]*).pkl"

_partition_data_tpl = "partition_dt${res}.pkl"

_learned_parameter_tpl = "learned_dt${res}_batch${batch_idx}.pkl"

_evaluation_data_tpl = "evaluation_dt${res}_batch${batch_idx}.pkl"
_evaluation_data_re = "evaluation_dt([0-9]*)_batch([0-9]*).pkl"

_evaluation_em_data_tpl = "evaluation_em_dt${res}_batch${batch_idx}.pkl"
_evaluation_em_data_re = "evaluation_em_dt([0-9]*)_batch([0-9]*).pkl"
_em_intermediate_file_tpl = "em_temp_${strategy_type}_batch${batch_idx}_${iteration}.pkl"
_em_intermediate_file_re = "em_temp_(.+)_batch([0-9]*)_([0-9]*).pkl"

def get_data_fname(**_):
  """ Returns the name of the file containing the raw data.
  Accepted arguments:
    none
  """
  return get_data_dir() + data_file

def get_data_file(mode='w', **_):
  """ Returns a file descriptor-like object to the file containing the data.
  Arguments:
    mode: r/w mode
  """
  return gzip.open(get_data_dir() + data_file, mode)

def get_partition_file(mode='r', **kwargs):
  """ Opens a partition file.

  Accepted kwargs:
   - res
  """
  fname = get_data_dir() + Template(_partition_data_tpl).substitute(**kwargs)
  return open(fname, mode)

def get_learned_parameter_file(mode='r', **kwargs):
  """ Opens a partition file.

  Accepted kwargs:
   - res
  """
  fname = get_data_dir() + Template(_learned_parameter_tpl).substitute(**kwargs)
  return open(fname, mode)

def get_evaluation_data_file(mode='r', **kwargs):
  """ Opens a partition file.

  Accepted kwargs:
   - res
  """
  fname = get_data_dir() + Template(_evaluation_data_tpl).substitute(**kwargs)
  return open(fname, mode)

def get_evaluation_em_data_file(mode='r', **kwargs):
  """ Opens a partition file.

  Accepted kwargs:
   - res
   - batch_idx
  """
  fname = get_data_dir() + Template(_evaluation_em_data_tpl).substitute(**kwargs)
  return open(fname, mode)

def get_evaluation_fnames(res=None, batch=None):
  """ Returns the list of raw data files in the work directory, filtered (if
  supplied) by a driver id.
  Generator function. Each generator element is a list of
  (full path name, driver id)
  """
  files = os.listdir(get_data_dir())
  p = re.compile(_evaluation_data_re)
  for f in files:
    m = p.match(f)
    if m:
      _res = int(m.group(1))
      if res is not None and _res != res:
        continue
      _batch = int(m.group(2))
      if batch is not None and _batch != batch:
        continue
      yield (get_data_dir() + f, _res, _batch)

def get_em_evaluation_fnames(res=None, batch=None):
  """ Returns the list of raw data files in the work directory, filtered (if
  supplied) by a driver id.
  Generator function. Each generator element is a list of
  (full path name, driver id)
  """
  files = os.listdir(get_data_dir())
  #logging.info("data dir: %r",get_data_dir())
  #logging.info("Files:")
  #logging.info(files)
  p = re.compile(_evaluation_em_data_re)
  for f in files:
    m = p.match(f)
    if m:
      _res = int(m.group(1))
      if res is not None and _res != res:
        continue
      _batch = int(m.group(2))
      if batch is not None and _batch != batch:
        continue
      logging.info((get_data_dir() + f, _res, _batch))
      yield (get_data_dir() + f, _res, _batch)

def get_raw_data_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the raw data.
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
  """
  fname = get_data_dir() + Template(raw_data_tpl).substitute(**kwargs)
  return gzip.open(fname, mode)

def get_raw_track_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the
  raw track.
  (A raw track is a collection of unmapped points)
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
  """
  fname = get_data_dir() + Template(raw_tracks_tpl).substitute(**kwargs)
  return gzip.open(fname, mode)

def get_mapped_points_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the
  raw track.
  (A raw track is a collection of unmapped points)
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
  """
  fname = get_data_dir() + Template(mapped_points_tpl).substitute(**kwargs)
  return gzip.open(fname, mode)

def get_traj_points_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the
  points associated to a trajectory.
  (A trajectory is a sequence of mapped points with positive flow)
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
    track_idx: integer, the index of the track
  """
  fname = get_data_dir() + Template(traj_points_tpl).substitute(**kwargs)
  return gzip.open(fname, mode)

def get_mapped_tracks_fname(mode='r', **kwargs):
  fname = get_data_dir() + Template(mapped_tracks_tpl).substitute(**kwargs)
  return fname

def get_mapped_tracks_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the
  raw track.
  (A mapped track is a collection of tuples). Each tuple is:
    - linking pairs
    - paths
    - linking pairs
    - points
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
  """
  fname = get_data_dir() + Template(mapped_tracks_tpl).substitute(**kwargs)
  return gzip.open(fname, mode)

def get_mapped_trajs_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the
  trajectory.
  (A mapped track is a collection of tuples). Each tuple is:
    - linking pairs
    - paths
    - linking pairs
    - points
  Furthermore, this sequence has positive flow through the linking pairs.
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
    track_idx: integer, the index of the track
  """
  fname = get_data_dir() + Template(mapped_trajs_tpl).substitute(**kwargs)
  return gzip.open(fname, mode)

def get_features_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the
  feature vectors of a trajectory.
  The feature vectors alternate points and path feature vectors, in a
  single list.
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
    track_idx: integer, the index of the track
    res: integer, temporal resolution (seconds). 0 means the reference
      track (undecimated).
  """
  fname = get_data_dir() + Template(features_tpl).substitute(**kwargs)
  return open(fname, mode)

def get_most_likely_indexes_file(mode='r', **kwargs):
  """ Returns a file descriptor-like object to the file containing the
  feature vectors of a trajectory.
  The feature vectors alternate points and path feature vectors, in a
  single list.
  Arguments:
    mode: r/w mode
    driver_id: string, the id of the driver
    track_idx: integer, the index of the track
    res: integer, temporal resolution (seconds). 0 means the reference
      track (undecimated).
  """
  fname = get_data_dir() + Template(most_likely_indexes_tpl).substitute(**kwargs)
  return open(fname, mode)

def get_raw_data_fnames(driver_id=None):
  """ Returns the list of raw data files in the work directory, filtered (if
  supplied) by a driver id.
  Generator function. Each generator element is a list of
  (full path name, driver id)
  """
  files = os.listdir(get_data_dir())
  p = re.compile(_raw_data_tpl_re)
  for f in files:
    m = p.match(f)
    if m:
      _driver_id = m.group(1)
      if driver_id and _driver_id != driver_id:
        continue
      yield (get_data_dir() + f, _driver_id)

def get_em_intermediate_fnames(type=None, iteration=None, batch_idx=None):
  """ Returns the list of the EM intermediate files computed from the big
  cloud data. (in pickle format)
  Generator function. Each generator element is a list of
  (full path name, )
  """
  files = os.listdir(get_data_dir())
  p = re.compile(_em_intermediate_file_re)
  for f in files:
    m = p.match(f)
    if m:
      _type = m.group(1)
      _batch_idx = int(m.group(2))
      _iteration = int(m.group(3))
      if type is not None and _type != type:
        continue
      if iteration is not None and _iteration != iteration:
        continue
      if batch_idx is not None and _batch_idx != batch_idx:
        continue
      yield (get_data_dir() + f, _type, _batch_idx, _iteration)

def get_em_intermediate_file(type, iteration, batch_idx, mode='r'):
  fname = get_data_dir() + "/" + Template(_em_intermediate_file_tpl).substitute(strategy_type=type, iteration=iteration, batch_idx=batch_idx)
  return open(fname, mode)


def get_raw_tracks_fnames(driver_id=None):
  """ Returns the list of raw track files in the work directory, filtered (if
  supplied) by a driver id.
  Generator function. Each generator element is a list of
  (full path name, driver id, track idx, number of tracks)
  """
  files = os.listdir(get_data_dir())
  p = re.compile(_raw_tracks_tpl_re)
  for f in files:
    m = p.match(f)
    if m:
      _driver_id = m.group(1)
      if driver_id and _driver_id != driver_id:
        continue
      yield (get_data_dir() + f, _driver_id)

def get_mapped_points_fnames(driver_id=None):
  """ Returns the list of mapped point files in the work directory, filtered
  if supplied) by a driver id.
  Generator function. Each generator element is a list of
  (full path name, driver id)
  """
  files = os.listdir(get_data_dir())
  p = re.compile(_mapped_points_tpl_re)
  for f in files:
    m = p.match(f)
    if m:
      _driver_id = m.group(1)
      if driver_id and _driver_id != driver_id:
        continue
      yield (get_data_dir() + f, _driver_id)

def get_mapped_tracks_fnames(driver_id=None):
  files = os.listdir(get_data_dir())
  p = re.compile(_mapped_tracks_tpl_re)
  for f in files:
    m = p.match(f)
    if m:
      _driver_id = m.group(1)
      if driver_id and _driver_id != driver_id:
        continue
      yield (get_data_dir() + f, _driver_id)


def get_features_fnames(driver_id=None, track_idx=None, dt=None):
  files = os.listdir(get_data_dir())
  p = re.compile(_mapped_points_tpl_re)
  for f in files:
    m = p.match(f)
    if m:
      _driver_id = m.group(1)
      _track_idx = int(m.group(2))
      _res = int(m.group(3))
      if driver_id and _driver_id != driver_id:
        continue
      if track_idx is not None and _track_idx != track_idx:
        continue
      if dt is not None and _res != dt:
        continue
      yield (get_data_dir() + f, _driver_id, _track_idx, _res)

def get_mapped_trajs_fnames(driver_id=None, track_idx=None, res=None):
  files = os.listdir(get_data_dir())
  p = re.compile(_mapped_trajs_tpl_re)
  for f in files:
    m = p.match(f)
    if m:
      _driver_id = m.group(1)
      _track_idx = int(m.group(2))
      _res = int(m.group(3))
      if driver_id and _driver_id != driver_id:
        continue
      if track_idx is not None and _track_idx != track_idx:
        continue
      if res is not None and _res != res:
        continue
      yield (get_data_dir() + f, _driver_id, _track_idx, _res)

def map_file_from_raw(mapping_closure, driver_id=None):
  """ Takes a raw track file and maps in into mapped points.
  """
  input_fdata = get_raw_tracks_fnames(driver_id=driver_id)
  for (in_fname, _driver_id) in input_fdata:
    fin = get_raw_track_file(mode='r', driver_id=_driver_id)
    print in_fname # Open and process this file line by line
    fin.readline() # Skip the first line
    fout = get_mapped_points_file(mode='w', driver_id=_driver_id)
    fout.write("[\n")
    for line in fin:
      if line == "0]": # End of the file? finish
        break
      dct = json.loads(line[:-2]) # Process one line, Remove the last column
      dct_out = mapping_closure(dct)
      if dct_out is not None:
        fout.write(json.dumps(dct_out))
        fout.write(",\n")
    fout.write("0]")
    fout.close()
    fin.close()


def map_file(mapping_closure, fdata_in, out_closure=None):
  for _args in fdata_in:
    print "mapping ", _args
    # Unpack the arguments, depends on the type of file.
    in_fname = _args[0]
    (_driver_id, _track_idx, _res) = (None, None, None)
    if len(_args) > 1:
      _driver_id = _args[1]
    else:
      _driver_id = None
    if len(_args) > 2:
      _track_idx = _args[2]
    else:
      _track_idx = None
    if len(_args) > 3:
      _res = _args[3]
    else:
      _res = None
    # Open and process this file line by line
    if in_fname.endswith('.gz'):
      fin = gzip.open(in_fname, 'r')
    else:
      fin = open(in_fname, 'r')
    fout = None
    if out_closure:
      fout = out_closure(mode='w', driver_id=_driver_id, \
                         track_idx=_track_idx, \
                         res=_res)
      print "output: ", fout
      fout.write("[\n")
    # Skip the first line
    fin.readline()
    for line in fin:
      # End of the file? finish
      if line == "0]":
        break
      # Process one line
      # Remove the last column
      dct = json.loads(line[:-2])
      dct_out = mapping_closure(dct)
      if dct_out is not None and fout:
        fout.write(json.dumps(dct_out))
        fout.write(",\n")
      del dct
      del dct_out
#      print gc.get_count()
#      gc.collect()
    fin.close()
    if fout:
      fout.write("0]")
      fout.close()

def cut_track_into_trajs(driver_id, segments):
  """ TODO: doc
  """
  fin = get_mapped_tracks_file(mode='r', driver_id=driver_id)
  print("<<<%s"%str(fin))
  # Skip the first line
  fin.readline()
  track_counter = 0
  elts_counter = 0
  for segment in segments:
    track_counter += 1
    fout = get_mapped_trajs_file(mode='w', \
                                 driver_id=driver_id, \
                                 track_idx=track_counter, res=0)
    print("OUT>>>%s"%str(fout))
    fout.write("[\n")
    for idx in segment:
      while elts_counter < idx:
        fin.readline()
        elts_counter += 1
      fout.write(fin.readline())
      elts_counter += 1
    fout.write("0]")
    fout.close()
  fin.close()

def cut_track_into_traj_points(driver_id, segments):
  """ TODO: doc
  """
  fin_points = get_mapped_points_file(mode='r', driver_id=driver_id)
  print("<<<%s"%str(fin_points))
  # Skip the first line
  fin_points.readline()
  track_counter = 0
  elts_counter = 0
  for segment in segments:
    track_counter += 1
    fout_points = get_traj_points_file(mode='w', \
                                       driver_id=driver_id, \
                                       track_idx=track_counter, res=0)
    print("OUT>>>%s"%str(fout_points))
    fout_points.write("[\n")
    for idx in segment:
      while elts_counter < idx:
        fin_points.readline()
        elts_counter += 1
      fout_points.write(fin_points.readline())
      elts_counter += 1
    fout_points.write("0]")
    fout_points.close()
  fin_points.close()

def create_traj_path_iterator(driver_id, track_idx, res):
  def traj_path_iterator():
    fin = get_mapped_trajs_file(mode='r', driver_id=driver_id, \
                                 track_idx=track_idx, res=res)
    fin.readline()
    fin.readline() # The first element only contains the first point
#    print "Traj iterator:",fin
    for line in fin:
      if line == '0]':
        break
      dct = json.loads(line[:-2])
      (_, paths_dct, _, _) = dct
      yield paths_dct
    fin.close()
  return traj_path_iterator

def get_network_dct(net_id):
  ''' Loads a network.

  TODO: move to MM-specific parts.
  '''
  fname = get_data_dir() + '/network_%s.json'%str(net_id)
  fin = open(fname, "r")
  dct = json.load(fin)
  fin.close()
  return dct

