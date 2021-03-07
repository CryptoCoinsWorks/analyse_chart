from pprint import pprint
from ui import search
from utils import signal
import qtawesome as qta
from libs import busy_indicator
from PySide2 import QtWidgets, QtCore, QtGui
from ui.qtmodern import windows as ws


class SearchWindow(search.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent=None, all_tickers=None):
        super(SearchWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.all_tickers = all_tickers

        self.signal = signal.EventHandler()
        self.busy = busy_indicator.BusyIndicator(parent=self)

        self.ticker = None
        self.compagny = None

        search_icon = qta.icon('mdi.access-point-network')
        self.label.setPixmap(QtGui.QPixmap("../ui/imgs/search.jpg").scaled(25, 25))
        # self.label.setIcon(search_icon)

        self.searchline.textChanged.connect(self.filter_treewidget)

        self.treeWidget.clicked.connect(self.get_item_value)
        self.build_columns()
        self.build_rows()

    # Build TreeWidget
    def build_columns(self):
        self.items = ['Ticker', 'Compagny']
        self.treeWidget.setHeaderLabels(self.items)

    def build_rows(self):
        for i, (ticker, name) in enumerate(self.all_tickers.items()):
            item = QtWidgets.QTreeWidgetItem(self.treeWidget, [ticker, name])

    # Filter TreeWidget from LineEdit
    def filter_treewidget(self, text):
        founds = self.treeWidget.findItems(text, QtCore.Qt.MatchContains, column=1)
        foundss = self.treeWidget.findItems(text, QtCore.Qt.MatchContains, column=0)
        found = founds+foundss

        all_items = self.get_all_items(self.treeWidget.invisibleRootItem())

        for item in all_items:
            item.setHidden(True)

        for item in found:
            item.setHidden(False)

        if not text:
            for item in all_items:
                item.setHidden(False)

    def get_all_items(self, item):
        result = [item]
        for index in range(item.childCount()):
            child = item.child(index)
            result.extend(self.get_all_items(child))
        return result

    # Set Variables
    def get_item_value(self):
        self.busy.show()
        self.ticker = self.treeWidget.selectedItems()[0].text(0)
        self.compagny = self.treeWidget.selectedItems()[0].text(1)
        self.signal.signal_search.emit(self.ticker)
        self.busy.hide()
        self.close()


