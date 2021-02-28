import os
import pyqtgraph as pg


class BarGraph(pg.BarGraphItem):
    def mouseClickEvent(self, event):
        print(self.getData())


def load_stylesheet(script_path=None):
    style = open(os.path.join(script_path, 'ui/style.css')).read()
    return style


def refacto_dette(dette_toref, leverage_toref):
    dette = []
    leverage = []
    for dett in dette_toref:
        if dett == "-":
            dette.append(0)
        else:
            dette.append(dett)
    for lev in leverage_toref:
        try:
            leverage.append(float(lev[:-1].replace(',', '.')))
        except:
            leverage.append(lev)
    return dette, leverage


def remove_nan(data):
    """
    Cette fonction renplace les valeurs NaN par 0.
    Sinon return float.
    :param data:
    :return: List
    """
    data_format = []
    for i in data:
        if str(i) == "nan":
            i = 0
        data_format.append(float(i))
    return data_format


def format_data(data):
    """
    Cette fonction format les nombres avec des ','.
    exemple:  2,120,350
    :param data:
    :return: List of string
    """
    data_format = []
    for i in remove_nan(data):
        i = f"{int(i):,}"
        data_format.append(i)
    return data_format

def get_last_value(data):
    if data[0] != 0:
        index = 0
        value = data[index]
    else:
        index = 1
        value = data[index]
    return value, index


def croissance(data):
    ls_croi = []
    el_prec = data[0]
    for element in data:
        if el_prec < element:
            ls_croi.append(True)
        else:
            ls_croi.append(False)
        el_prec = element
    decroi = ls_croi.count(False)
    croi = ls_croi.count(True)
    return croi, decroi


