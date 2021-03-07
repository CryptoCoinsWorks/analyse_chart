from PySide2 import QtWidgets, QtCore, QtGui
from pprint import pprint


class TableView(QtWidgets.QTableWidget):
    def __init__(self, parent, data):
        super(TableView, self).__init__(parent=parent)
        self.data = data

        # self.set_style()

        # Columns
        header = self.data['YEAR']
        hearder_len = len(header)
        header.insert(0, 'Valorisation')
        header.insert(hearder_len, 'Bilan')
        score = self.data["Score"]
        del self.data["YEAR"]
        del self.data["Score"]

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

        # Add Score to the last Row
        last_row = len(self.data)
        self.insertRow(last_row)
        cell_score_title = QtWidgets.QTableWidgetItem()
        cell_score_title.setData(QtCore.Qt.DisplayRole, "Score")
        self.setItem(last_row, 0, cell_score_title)
        cell_score = QtWidgets.QTableWidgetItem()
        cell_score.setData(QtCore.Qt.DisplayRole, str(score[0]))
        cell_score.setTextAlignment(QtCore.Qt.AlignRight)
        self.setItem(last_row, hearder_len+1, cell_score)

    def set_style(self):
        style = "::section {""background-color: #0b0d14; color:white; }"
        self.horizontalHeader().setStyleSheet(style)
        self.verticalHeader().setStyleSheet(style)

