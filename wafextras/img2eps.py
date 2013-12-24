""" Converts any image to EPS, using ImageMagick as a backend.
"""
from waflib import Logs
from waflib import TaskGen,Task
from waflib import Utils
from waflib.Configure import conf

def configure(conf):
  conf.find_program('convert',var='CONVERT')

@conf
def img2eps(bld, nodes):
  for source in nodes:
    outnode = source.change_ext(".eps")
    bld(rule="${CONVERT} ${SRC} ${TGT}",source=source,target=outnode)
