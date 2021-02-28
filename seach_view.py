from pprint import pprint
from ui import search
import qtawesome as qta
from PySide2 import QtWidgets, QtCore, QtGui


class SearchWindow(search.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, parent=None, all_tickers=None):
        super(SearchWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.all_tickers = all_tickers

        self.ticker = None
        self.compagny = None

        search_icon = qta.icon('mdi.access-point-network')
        # self.label.setPixmap(QtGui.QPixmap(search_icon))
        # self.label.setIcon(search_icon)

        # Complete
        # completer = QtWidgets.QCompleter(all_tickers)
        # completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        # self.lineEdit.setCompleter(completer)

        self.treeWidget.clicked.connect(self.get_item_value)
        self.build_columns()
        self.build_rows()

    def build_columns(self):
        items = ['Ticker', 'Compagny']
        self.treeWidget.setHeaderLabels(items)

    def build_rows(self):
        for i, (ticker, name) in enumerate(self.all_tickers.items()):
            item = QtWidgets.QTreeWidgetItem(self.treeWidget, [ticker, name])

    def get_item_value(self):
        self.ticker = self.treeWidget.selectedItems()[0].text(0)
        self.compagny = self.treeWidget.selectedItems()[0].text(1)
        self.quit_app()

    def quit_app(self):
        self.close()
