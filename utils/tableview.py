from PySide2 import QtWidgets, QtCore, QtGui
from pprint import pprint


class TableView(QtWidgets.QTableWidget):
    def __init__(self, parent, data):
        super(TableView, self).__init__(parent=parent)
        self.data = data["data"]
        self.analyse = data["analyse"]
        # pprint(data)

        self.set_style()

        list_remove = ["Nombre d'employés", "prix"]
        for element in list_remove:
            if element in self.data: del self.data[element]

        # Columns
        header = self.data['Année']
        header.insert(0, 'Valorisation')
        header.insert(len(header), 'Bilan')
        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)
        self.horizontalHeader().resizeSection(0, 150)

        # Rows
        for row, (title, donnee) in enumerate(sorted(self.data.items())[1:]):
            self.insertRow(row)
            cell_val = QtWidgets.QTableWidgetItem()
            cell_val.setData(QtCore.Qt.DisplayRole, title)
            self.setItem(row, 0, cell_val)
            for column, i in enumerate(donnee):
                cell = QtWidgets.QTableWidgetItem()
                cell.setData(QtCore.Qt.DisplayRole, i)
                self.setItem(row, column+1, cell)

            if title not in self.analyse.keys():
                continue
            analyse_cell = QtWidgets.QTableWidgetItem()
            analyse_cell.setData(QtCore.Qt.DisplayRole, self.analyse[title])
            self.setItem(row, 7, analyse_cell)


    def set_style(self):
        style = "::section {""background-color: #0b0d14; color:white; }"
        self.horizontalHeader().setStyleSheet(style)
        self.verticalHeader().setStyleSheet(style)

