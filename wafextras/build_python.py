#!/usr/bin/env python
# -*- coding: utf-8 -*- 

""" Module for building some files out of the execution of a python script.
"""

from waflib.Configure import conf
from waflib import Utils

def options(opt):
  opt.add_option('--data-dir', action='store', default='', dest='data_dir')

def configure(conf):
  conf.start_msg('Checking for the variable DATA_DIR')
  if conf.options.data_dir:
    conf.env.DATA_DIR = conf.options.data_dir
    conf.end_msg(conf.env.DATA_DIR)
  else:
    conf.end_msg('DATA_DIR is not set')

@conf
def build_python(bld, source_, targets_):
  source = bld.path.make_node(source_)
  folder = bld.path.get_bld().make_node("pyimg/")
  bld.to_log("My log")
  targets = [folder.make_node(target).get_bld() for target in Utils.to_list(targets_)]
  bld(rule = "PYTHONPATH=$PYTHONPATH:%s/python SAVE_DIR=%s DATA_DIR=%s MATPLOTLIB_HEADLESS=1 python -B %s --log=INFO"%(bld.path.abspath(), folder.abspath(), bld.env.DATA_DIR, source.abspath()),
      source = [source],
      target = targets,
      name = "%s-python"%source)
