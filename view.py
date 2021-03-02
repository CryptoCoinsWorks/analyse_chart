from pprint import pprint
from ui import graphic_view
from PySide2 import QtWidgets, QtCore, QtGui
import seach_view
from ui.qtmodern import windows as ws

class EventHandler(QtCore.QObject):
    signal_search = QtCore.Signal(object)

class Window(graphic_view.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent=None, ticker=None, all_tickers=None):
        super(Window, self).__init__(parent=parent)
        self.setupUi(self)
        self.signal = EventHandler()
        self.center()

        self.all_tickers = all_tickers

        self.lineEdit.setText(ticker)
        self.lineEdit.mousePressEvent = self.labelPressedEvent
        # self.lineEdit.mousePressEvent = self.paintEvent(self)

    def center(self):
        qRect = self.frameGeometry()
        centerpoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerpoint)
        self.move(qRect.topLeft())

    def labelPressedEvent(self, event):
        """Set editable if the left mouse button is clicked"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.open()

    def open(self):
        self.parent().setEnabled(False)
        self.search = seach_view.SearchWindow(self, self.all_tickers)
        # self.search.signal.signal_search.connect()

        mw = ws.ModernWindow(self.search)

        mw.show()

