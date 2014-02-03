""" Converts any image to EPS, using ImageMagick as a backend.
"""
from waflib import Logs
from waflib import TaskGen,Task
from waflib import Utils
from waflib.Configure import conf
import urllib

class DownloadData(Task.Task):
  
  def run(self):
    fout = self.outputs[0].abspath()
    Logs.debug("Retrieving file %r to %r" % (self.url, fout))
    urllib.urlretrieve(self.url,fout)

@conf
def download_data(bld, remote_url, local_name):
  tsk0 = bld()
  tsk = tsk0.create_task("DownloadData")
  tsk.url = remote_url
  out_node = bld.path.get_bld().make_node(local_name)
  print "outnode: ", out_node.abspath()
  tsk.set_inputs([])
  tsk.set_outputs(out_node)

