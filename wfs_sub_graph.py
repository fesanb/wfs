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
