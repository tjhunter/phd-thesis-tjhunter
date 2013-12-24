""" Converts any image to EPS, using ImageMagick as a backend.
"""
from waflib import Logs
from waflib import TaskGen,Task
from waflib import Utils
from waflib.Configure import conf

def configure(conf):
  conf.find_program('unoconv',var='UNOCONV')

@conf
def oo2pdf(bld, nodes):
  for source in nodes:
    outnode = source.change_ext(".pdf").get_bld()
    bld(rule="${UNOCONV} --stdout -f pdf ${SRC[0].abspath()} > ${TGT[0].abspath()}",source=source,target=outnode)
