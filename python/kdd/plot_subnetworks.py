__author__ = 'tjhunter'

import build
import json
import pylab as pl
import numpy as np
# Draws the network as a pdf and SVG file.

fname = build.data_name('kdd/hmm_graph_export.json')
fig = pl.figure("fig1",figsize=(10,10))
ax = fig.gca()
ax.set_axis_off()
node_style={'c':'g', 's':80}
link_style=dict(lw=.01)
with open(fname) as f:
  lats = []
  lons = []
  lats_ = []
  lons_ = []
  dlats = []
  dlons = []
  for l in f:
    dct = json.loads(l)
    lats_.append(dct['lat'])
    lons_.append(dct['lon'])
    lats.append(dct['lats'])
    lons.append(dct['lons'])
    dlats.append(dct['dlat'])
    dlons.append(dct['dlon'])
  ax.quiver(np.array(lons_), np.array(lats_), np.array(dlons), np.array(dlats),
            scale_units='xy', angles='xy', scale=1, **link_style)
with open(build.data_name('kdd/hmm_graph_export_vertices.json')) as f:
  dct = json.load(f)
  lons = dct['lons']
  lats = dct['lats']
  ax.scatter(lons, lats, zorder=11, **node_style)
build.save_figure(fig, 'figures-kdd/hmm_graph',save_svg=True)


var_style = {'marker':'o','zorder':2}
edge_style = {'c':'g','zorder':1}
fig = pl.figure('fig2',figsize=(5,5))
ax = fig.gca()
ax.set_axis_off()
with open(build.data_name('kdd/ttgraph_export_edges.json')) as f:
  lats = []
  lons = []
  for l in f:
    dct = json.loads(l)
    lats.append(dct['lats'])
    lons.append(dct['lons'])
  ax.plot(np.array(lons).T, np.array(lats).T, **edge_style)
with open(build.data_name('kdd/ttgraph_export_vertices.json')) as f:
  dct = json.load(f)
  node_lats = dct['lats']
  node_lons = dct['lons']
  ax.scatter(node_lons, node_lats, **var_style)
build.save_figure(fig, 'figures-kdd/tt_graph',save_svg=True)
