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


global g1, g2, g3, g4


def graph_plot(gw_x, gw_y, ga_y):
	global g1, g2, g3, g4
	pg.setConfigOption('background', 'k')
	g = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
	g.showGrid(x=True, y=True)

	# WIND
	pg.setConfigOption('foreground', 'y')
	g1 = g.plotItem
	g1.setLabels(left='WIND')
	g1.setYRange(min(gw_y) - 8, max(gw_y)+8)

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

	# TEMP
	pg.setConfigOption('foreground', 'r')
	g3 = pg.ViewBox()
	ax3 = pg.AxisItem('right')
	g1.layout.addItem(ax3, 2, 3)
	g1.scene().addItem(g3)
	ax3.linkToView(g3)
	g3.setXLink(g1)
	# ax3.setLabel('TEMP', color='#ff0000')
	g3.setYRange(-5, 30)

	# HUM
	pg.setConfigOption('foreground', 'g')
	g4 = pg.ViewBox()
	ax4 = pg.AxisItem('right')
	g1.layout.addItem(ax4, 2, 4)
	g1.scene().addItem(g4)
	ax4.linkToView(g4)
	g4.setXLink(g1)
	# ax4.setLabel('HUM', color='#00ff00')
	g4.setYRange(0, 100)

	g1.plot(gw_x, gw_y, clear=True, pen='y')
	# g2.addItem(pg.PlotCurveItem(ga_x, ga_y, clear=True, pen='b'))
	# g3.addItem(pg.PlotCurveItem(gt_x, gt_y, clear=True, pen='r'))
	# g4.addItem(pg.PlotCurveItem(gh_x, gh_y, clear=True, pen='g'))

	g2.setGeometry(g1.vb.sceneBoundingRect())
	g3.setGeometry(g1.vb.sceneBoundingRect())
	g4.setGeometry(g1.vb.sceneBoundingRect())

	return g


def graph_update(self, gw_x, gw_y, ga_x, ga_y, gt_x, gt_y, gh_x, gh_y):

	if self.gw is True:
		g1.plot(gw_x, gw_y, clear=True, pen='y')
	else:
		g1.clear()

	if self.ga is True:
		g2.setYRange(min(ga_y) - 8, max(ga_y)+8)
		g2.addItem(pg.PlotCurveItem(ga_x, ga_y, clear=True, pen='b'))
		g2.setGeometry(g1.vb.sceneBoundingRect())
	else:
		g2.clear()

	if self.gt is True:
		g3.addItem(pg.PlotCurveItem(gt_x, gt_y, clear=True, pen='r'))
		g3.setGeometry(g1.vb.sceneBoundingRect())
	else:
		g3.clear()

	if self.gh is True:
		g4.addItem(pg.PlotCurveItem(gh_x, gh_y, clear=True, pen='g'))
		g4.setGeometry(g1.vb.sceneBoundingRect())
	else:
		g4.clear()

	# return self.graph
