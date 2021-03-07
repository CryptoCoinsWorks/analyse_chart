
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import time

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        kwds['enableMenu'] = False
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()

    ## reimplement mouseDragEvent to disable continuous axis zoom
    def mouseDragEvent(self, ev, axis=None):
        if axis is not None and ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev, axis=axis)

class CustomTickSliderItem(pg.TickSliderItem):
    def __init__(self, *args, **kwds):
        pg.TickSliderItem.__init__(self, *args, **kwds)

        self.all_ticks = {}
        self._range = [0, 1]

    def setTicks(self, ticks):
        pprint(ticks)
        for tick, pos in self.listTicks():
            self.removeTick(tick)

        for pos in ticks:
            tickItem = self.addTick(pos, movable=False, color="333333")
            self.all_ticks[pos] = tickItem

        self.updateRange(None, self._range)

    def updateRange(self, vb, viewRange):
        origin = self.tickSize / 2.
        length = self.length

        lengthIncludingPadding = length + self.tickSize + 2

        self._range = viewRange

        for pos in self.all_ticks:
            tickValueIncludingPadding = (pos - viewRange[0]) / (viewRange[1] - viewRange[0])
            tickValue = (tickValueIncludingPadding * lengthIncludingPadding - origin) / length

            # Convert from np.bool_ to bool for setVisible
            visible = bool(tickValue >= 0 and tickValue <= 1)

            tick = self.all_ticks[pos]
            tick.setVisible(visible)

            if visible:
                self.setTickValue(tick, tickValue)


from pprint import pprint
# dates = np.arange(8) * (3600*24*356)
# pprint(dates)



