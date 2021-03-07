from PySide2 import QtCore

class EventHandler(QtCore.QObject):
    signal_search = QtCore.Signal(str)