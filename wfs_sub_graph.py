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


def graph_plot(gw_x, gw_y, ga_x, ga_y, gt_x, gt_y, gh_x, gh_y):
    global g1, g2, g3, g4
    pg.setConfigOption('background', '#000000')
    g = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
    g.showGrid(x=True, y=True)

    g1 = g.plotItem
    g1.setLabels(left='WIND')

    g2 = pg.ViewBox()
    g1.showAxis('right')
    g1.scene().addItem(g2)
    g1.getAxis('right').linkToView(g2)
    g2.setXLink(g1)
    g1.getAxis('right').setLabel('ATP', color='#0000ff')

    g3 = pg.ViewBox()
    ax3 = pg.AxisItem('right')
    g1.layout.addItem(ax3, 2, 3)
    g1.scene().addItem(g3)
    ax3.linkToView(g3)
    g3.setXLink(g1)
    ax3.setLabel('TEMP', color='#ff0000')

    g4 = pg.ViewBox()
    ax4 = pg.AxisItem('left')
    g1.layout.addItem(ax4, 2, 3)
    g1.scene().addItem(g4)
    ax4.linkToView(g4)
    g4.setXLink(g1)
    ax4.setLabel('HUM', color='#00ff00')

    g2.setGeometry(g1.vb.sceneBoundingRect())
    g3.setGeometry(g1.vb.sceneBoundingRect())
    g4.setGeometry(g1.vb.sceneBoundingRect())

    g1.plot(gw_x, gw_y, clear=True, pen='y')
    g2.addItem(pg.PlotCurveItem(ga_x, ga_y, clear=True, pen='b'))
    g3.addItem(pg.PlotCurveItem(gt_x, gt_y, clear=True, pen='r'))
    g4.addItem(pg.PlotCurveItem(gh_x, gh_y, clear=True, pen='g'))
    return g


# def graph_update(gw_x, gw_y, ga_x, ga_y, gt_x, gt_y, gh_x, gh_y):
#     g = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
#     g.showGrid(x=True, y=True)
#
#     g1 = g.plotItem
#
#     g1.plot(gw_x, gw_y, clear=True, pen='y')
#     g2.addItem(pg.PlotCurveItem(ga_x, ga_y, clear=True, pen='b'))
#     g3.addItem(pg.PlotCurveItem(gt_x, gt_y, clear=True, pen='r'))
#     g4.addItem(pg.PlotCurveItem(gh_x, gh_y, clear=True, pen='g'))
#     return g

def graph_update(self, gw_x, gw_y, ga_x, ga_y, gt_x, gt_y, gh_x, gh_y):
    global g1, g2, g3, g4
    g1.plot(gw_x, gw_y, clear=True, pen='b')
    g2.addItem(pg.PlotCurveItem(ga_x, ga_y, clear=True, pen='b'))
    g3.addItem(pg.PlotCurveItem(gt_x, gt_y, clear=True, pen='r'))
    g4.addItem(pg.PlotCurveItem(gh_x, gh_y, clear=True, pen='g'))

    g1.enableAutoRange('xy', False)
    g2.enableAutoRange('xy', False)
    g3.enableAutoRange('xy', False)
    g4.enableAutoRange('xy', False)

    return self.graph

# def graph_update(self, x, y):
#     self.graph.plot(x, y, clear=True, pen='y')
#     return self.graph
