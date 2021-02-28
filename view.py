from pprint import pprint
from ui import graphic_view
from PySide2 import QtWidgets, QtCore, QtGui
import seach_view

class Window(graphic_view.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent=None, all_tickers=None):
        super(Window, self).__init__(parent=parent)
        self.setupUi(self)
        self.all_tickers = all_tickers

        self.lineEdit.setText('kuhjkhjkh')
        self.lineEdit.mousePressEvent = self.labelPressedEvent


    def labelPressedEvent(self, event):
        """Set editable if the left mouse button is clicked"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.search = seach_view.SearchWindow(self, self.all_tickers)
            self.search.show()

        print(self.search.ticker)


