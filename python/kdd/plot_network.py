
__author__ = 'tjhunter'

import build
import json
import pylab as pl
from matplotlib.collections import LineCollection
# Draws the network as a pdf and SVG file.

def draw_network(ax, fd, link_style):
  def decode_line(l):
    #print l
    dct = json.loads(l)
    lats = dct['lats']
    lons = dct['lons']
    return zip(lons, lats)
  lines = [decode_line(l) for l in fd]
  #print lines
  xmin = min([x for l in lines for x,y in l])
  xmax = max([x for l in lines for x,y in l])
  ymin = min([y for l in lines for x,y in l])
  ymax = max([y for l in lines for x,y in l])
  lc = LineCollection(lines, **link_style)
  ax.add_collection(lc, autolim=True)
  return ((xmin,xmax),(ymin,ymax))


fname = build.data_name('kdd/net_export_6.json')
fig = pl.figure("fig1",figsize=(10,10))
ax = fig.gca()
ax.set_axis_off()
style = {'colors':'k','linewidths':0.5}
with open(fname) as f:
  (xlims, ylims) = draw_network(ax, f, style)
  ax.set_xlim(*xlims)
  ax.set_ylim(*ylims)
# Saving in pdf is a bit slow
build.save_figure(fig, 'figures-kdd/network_export_6',save_svg=False)

