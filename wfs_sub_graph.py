# WFS - Weather Forecast Station
# Written by Stefan Bahrawy

import pyqtgraph as pg
from datetime import datetime


class TimeAxisItem(pg.AxisItem):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.setLabel(text='Time', units=None)
		self.enableAutoSIPrefix(False)

	def tickStrings(self, values, scale, spacing):
		return [datetime.fromtimestamp(value).strftime("%H:%M") for value in values]


global g1, g2


def graph_plot(gw_x, gw_y, ga_y):
	global g1, g2
	pg.setConfigOption('background', 'k')
	g = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
	g.showGrid(x=True, y=True)

	# WIND
	pg.setConfigOption('foreground', 'y')
	g1 = g.plotItem
	g1.setLabels(left='WIND')
	g1.setYRange(min(gw_y), max(gw_y))

	# ATP
	pg.setConfigOption('foreground', 'b')
	g2 = pg.ViewBox()
	ax2 = pg.AxisItem('right')
	g1.layout.addItem(ax2, 2, 2)
	g1.scene().addItem(g2)
	ax2.linkToView(g2)
	g2.setXLink(g1)
	# ax2.setLabel('TEMP', color='#ff0000')
	g2.setYRange(min(ga_y) - 8, max(ga_y)+8)

	g1.plot(gw_x, gw_y, clear=True, pen='y')
	g2.setGeometry(g1.vb.sceneBoundingRect())

	return g


def graph_update(self, gw_x, gw_y, ga_x, ga_y):

	if self.gw is True:
		g1.setYRange(min(gw_y), max(gw_y))
		g1.plot(gw_x, gw_y, clear=True, pen='y')
	else:
		g1.clear()

	if self.ga is True:
		g2.setYRange(min(ga_y) - 8, max(ga_y)+8)
		g2.addItem(pg.PlotCurveItem(ga_x, ga_y, clear=True, pen='b'))
		g2.setGeometry(g1.vb.sceneBoundingRect())
	else:
		g2.clear()
