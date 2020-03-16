from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import mysql.connector
from datetime import datetime, timedelta


class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime("%H:%M") for value in values]


cnx = mysql.connector.connect(user='wfs', database='wfs', password='wfs22')
cursor = cnx.cursor(buffered=True)
interval = 5000
get_mean = "SELECT mean, UNIX_TIMESTAMP(tmestmp) FROM mean WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)
get_atp = "SELECT atp, UNIX_TIMESTAMP(tmestmp) FROM sens WHERE tmestmp >= DATE_SUB(NOW(), INTERVAL {} HOUR)".format(interval)

cursor.execute(get_mean)
db_graph_wind = cursor.fetchall()
mean_X = []
mean_Y = []

for i in db_graph_wind:
    mean_Y.append(i[0])
    mean_X.append(i[1])

print(len(mean_X))

cursor.execute(get_atp)
db_graph_atp = cursor.fetchall()
atp_X = []
atp_Y = []

for i in db_graph_atp:
    atp_Y.append(i[0])
    atp_X.append(i[1])

print(len(atp_X))

pg.mkQApp()

graph = pg.PlotWidget()
graph.show()

g1 = graph.plotItem
g1.setLabels(left='axis1')

g2 = pg.ViewBox()
g1.showAxis('right')
g1.scene().addItem(g2)
g1.getAxis('right').linkToView(g2)
g2.setXLink(g1)
g1.getAxis('right').setLabel('axis2', color='#0000ff')

def updateViews():
    ## view has resized; update auxiliary views to match
    global g1, g2
    g2.setGeometry(g1.vb.sceneBoundingRect())
    # p3.setGeometry(p1.vb.sceneBoundingRect())

    ## need to re-update linked axes since this was called
    ## incorrectly while views had different shapes.
    ## (probably this should be handled in ViewBox.resizeEvent)
    g2.linkedViewChanged(g1.vb, g2.XAxis)
    # p3.linkedViewChanged(p1.vb, p3.XAxis)

updateViews()
g1.vb.sigResized.connect(updateViews)

g1.plot(mean_X, mean_Y, pen='r')
g2.addItem(pg.PlotCurveItem(atp_X, atp_Y, pen='b'))


# graph = pg.PlotWidget(axisItems={'bottom': TimeAxisItem(orientation='bottom')})
# graph.showGrid(x=True, y=True)
# #
# graph.plot(mean_X, mean_Y, clear=True, pen='y')


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
