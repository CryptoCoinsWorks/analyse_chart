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
        self.label.setPixmap(QtGui.QPixmap("ui/imgs/search.jpg").scaled(25, 25))
        # self.label.setIcon(search_icon)

        self.searchline.textChanged.connect(self._filter_trw_lightsets)

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
    def _filter_trw_lightsets(self):
        """This private method sorts the tree thanks to the text in the
        lineedit filter"""
        text = str(self.searchline.text())
        self.filter_tree_widget(text=text, tree_widget=self.treeWidget)

    def filter_tree_widget(self, text, tree_widget):
        """This function is a simple filter for the tree_widget

        :param text: The text to find in the tree
        :type text: str
        :param tree_widget: The tree widget
        :type tree_widget: QtWidgets.QTreeWidget
        """
        keywords = text.split(";")
        keywords = [x.lower().strip() for x in keywords if x]

        all_items = self.get_all_items(keep_invisible_root=True)
        column_number = len(self.items)
        all_found = []
        final_items = []

        for keyword in keywords:
            found = []
            for item in all_items:
                for index in range(column_number):
                    item_text = item.text(index)
                    if keyword in item_text.lower():
                        found.append(item)
            all_found.append(list(set(found)))

        if all_found:
            final_items = set(all_found[0]).intersection(*all_found)

        if not text:
            for item in all_items:
                item.setHidden(False)
        else:
            for item in all_items:
                item.setHidden(True)
                # If we have an item found
                if not final_items:
                    return
                for item in list(final_items):
                    # show only item
                    item.setHidden(False)

    def get_all_items(self, keep_invisible_root=False):
        """This method return all items in the tree widget
        from the invisibleRootItem

        :return: The list of all items
        :rtype: list
        """
        item = self.treeWidget.invisibleRootItem()
        all_items = self._get_all_items(item=item)
        if not keep_invisible_root:
            all_items.pop(0)
        return all_items

    def _get_all_items(self, item):
        """This method return all items in the treewidget

        :param item: The first item
        :type item: object
        :return: The list of all items
        :rtype: list
        """
        result = [item]
        for index in range(item.childCount()):
            child = item.child(index)
            result.extend(self._get_all_items(child))
        return result

    # Set Variables
    def get_item_value(self):
        self.ticker = self.treeWidget.selectedItems()[0].text(0)
        self.compagny = self.treeWidget.selectedItems()[0].text(1)
        self.quit_app()

    def quit_app(self):
        self.close()
