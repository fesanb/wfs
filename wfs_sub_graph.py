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


def graph_plot(wind_graph_X, wind_graph_Y, atp_graph_X, atp_graph_Y):
    pg.setConfigOption('background', '#000000')
    graph = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
    graph.showGrid(x=True, y=True)

    # graph = graph.plotItem
    graph.setLabels(left='Wind')

    graph2 = pg.ViewBox()
    graph.showAxis('right')
    graph.scene().addItem(graph2)
    graph.getAxis('right').linkToView(graph2)
    graph2.setXLink(graph)
    graph.getAxis('right').setLabel('ATP', color='#0000ff')

    graph.plot(wind_graph_X, wind_graph_Y, clear=True, pen='w')
    graph2.addItem(pg.PlotCurveItem(atp_graph_X, atp_graph_Y, clear=True, pen='b'))
    return graph


def graph_update(self, wind_graph_X, wind_graph_Y, atp_graph_X, atp_graph_Y):
    self.graph.plot(wind_graph_X, wind_graph_Y, clear=True, pen='y')
    self.graph2.addItem(pg.PlotCurveItem(atp_graph_X, atp_graph_Y, clear=True, pen='b'))
    return self.graph
