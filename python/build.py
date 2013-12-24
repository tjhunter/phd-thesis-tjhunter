# The definitions of the input and output directories to control where the images are being written.
# Defines some imports for matplotlib as well.
import os
import logging
logging.getLogger().setLevel(logging.INFO)

if "SAVE_DIR" in os.environ:
  __path_savefig = os.environ['SAVE_DIR']
logging.info("Saving path: " + __path_savefig)
if "DATA_DIR" in os.environ:
  __path_data = os.environ["DATA_DIR"]
  logging.info("Data root path: %r", __path_data)

if "MATPLOTLIB_HEADLESS" in os.environ:
  print "Configuring matplotlib to headless"
  import matplotlib
  matplotlib.use("Agg")
  from matplotlib import rc
  #rc('font',**{'family':'serif','serif':['Times New Roman']})
  matplotlib.rcParams['ps.useafm'] = True
  matplotlib.rcParams['pdf.use14corefonts'] = True
  #matplotlib.rcParams['text.usetex'] = True
  rc('font', **{'family':'serif'})

def save_path():
  return __path_savefig

def data_path():
  return __path_data

def data_name(name):
  return "%s/%s"%(data_path(),name)

def save_name(name, ensure_dir=True):
  fname = "%s/%s"%(save_path(),name)
  fdir = os.path.dirname(fname)
  logging.debug("Asking for save name %s, (%s)" % (fname, fdir))
  if ensure_dir and not os.path.exists(fdir):
    logging.info("Creating directory %r ",fdir)
    os.makedirs(fdir)
  return fname

def save_figure(fig, name, save_pdf=True, save_svg=True):
  if save_pdf:
    fig.savefig("%s.pdf"%(save_name(name)), bbox_inches='tight')
  if save_svg:
    fig.savefig("%s.svg"%(save_name(name)), bbox_inches='tight')
