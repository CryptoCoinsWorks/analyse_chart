import os
import pyqtgraph as pg
from PySide2.QtCore import QFile


class BarGraph(pg.BarGraphItem):
    def mouseClickEvent(self, event):
        print(self.getData())

def load_stylesheet(script_path=None):
    style = open(os.path.join(script_path, 'ui/style.css')).read()
    return style

