from . import seach_view
from utils import signal
import pyqtgraph as pg
from ui import graphic_view
from PySide2 import QtWidgets, QtCore
from ui.qtmodern import windows as ws


class Window(graphic_view.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent=None, ticker=None, all_tickers=None):
        super(Window, self).__init__(parent=parent)
        self.setupUi(self)
        self.signal = signal.EventHandler()
        self.center()

        self.all_tickers = all_tickers
        self.dialog_ticker = seach_view.SearchWindow(self, self.all_tickers)

        self.lineEdit.setText(ticker)
        self.lineEdit.mousePressEvent = self.labelPressedEvent
        self.dialog_ticker.signal.signal_search.connect(self.get_ticker)




    # def set_button_clicked(self):

    def center(self):
        qRect = self.frameGeometry()
        centerpoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerpoint)
        self.move(qRect.topLeft())

    def labelPressedEvent(self, event):
        """Set editable if the left mouse button is clicked"""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            # mw = ws.ModernWindow(self.dialog_ticker)
            # mw.show()
            self.dialog_ticker.show()

    def get_ticker(self, ticker_name):
        self.lineEdit.setText(ticker_name)
        self.load_data(ticker_name)

