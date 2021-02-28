from PySide2 import QtWidgets, QtCore, QtGui
from pprint import pprint


class TableView(QtWidgets.QTableWidget):
    def __init__(self, parent, data):
        super(TableView, self).__init__(parent=parent)
        self.data = data

        self.set_style()

        # Columns
        header = self.data['YEAR']
        header.insert(0, 'Valorisation')
        header.insert(len(header), 'Bilan')
        del self.data["YEAR"]

        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)
        self.horizontalHeader().resizeSection(0, 150)
        self.setColumnWidth(len(header)-1, 250)
        self.setWordWrap(True)

        # Rows
        for row, (title, donnee) in enumerate(sorted(self.data.items())):
            self.insertRow(row)
            cell_val = QtWidgets.QTableWidgetItem()
            cell_val.setData(QtCore.Qt.DisplayRole, title)
            self.setItem(row, 0, cell_val)
            for column, data in enumerate(donnee):
                cell = QtWidgets.QTableWidgetItem()
                cell.setData(QtCore.Qt.DisplayRole, str(data))
                cell.setTextAlignment(QtCore.Qt.AlignRight)
                self.setItem(row, column+1, cell)

            analyse_cell = QtWidgets.QTableWidgetItem()
            analyse_cell.setData(QtCore.Qt.DisplayRole, self.data[title])
            self.setItem(row, 7, analyse_cell)


    def set_style(self):
        style = "::section {""background-color: #0b0d14; color:white; }"
        self.horizontalHeader().setStyleSheet(style)
        self.verticalHeader().setStyleSheet(style)

