"""BusyIndicator is a simple widget that show an animated svg to show that
the script works.
"""
import os
from PySide2 import QtCore, QtGui, QtSvg, QtWidgets


PATH = os.path.join(os.path.abspath(os.path.join(__file__, "../..")), 'ressources')

class BusyIndicator(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BusyIndicator, self).__init__(parent)

        self.resize(80, 80)

        layout = QtWidgets.QHBoxLayout()
        svg = QtSvg.QSvgWidget()
        path = os.path.join(PATH, 'svg', 'oval.svg')
        svg.load(path)
        layout.addWidget(svg)
        self.setLayout(layout)

        self.hide()

    def show(self):
        self.move(self.parent().rect().center() - self.rect().center())
        self.parent().setEnabled(False)
        super(BusyIndicator, self).show()

    def hide(self):
        self.parent().setEnabled(True)
        super(BusyIndicator, self).hide()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(),
                         QtGui.QBrush(QtGui.QColor(55, 55, 55, 255)))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.end()

if __name__ == '__main__':
    print(PATH)