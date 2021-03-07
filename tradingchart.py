# Yahoo Finance API
# https://algotrading101.com/learn/yahoo-finance-api-guide/
# todo :
# - Dessiner droite sur graph
# - CrooHaire sur tout les plots
# - Faire machiner learn pour "prevision" futur
# - retrouver pattern avec talib


import os
import json
from datetime import datetime
from pprint import pprint

import pandas as pd
import numpy as np
import pyqtgraph as pg
from PySide2 import QtWidgets

from views import main_view, tableview
from libs import busy_indicator

from utils import utils
from utils import indicators
from utils import candlestick
from utils import custom_axis
from utils.utils import BarGraph
from ui.qtmodern import windows as ws
from ui.qtmodern import styles as stl
from modules import strategies as stg
from modules.analyse_financials import AnalyseFondamental
from modules.yahoo_fin import stock_info as sf


PATH = os.path.join(os.path.dirname(__file__), 'datas')

# class DrawGraphView(QtWidgets.)

class GraphWindow(main_view.Window, QtWidgets.QMainWindow):
    def __init__(self, ticker, all_tickers):
        super(GraphWindow, self).__init__(ticker=ticker, all_tickers=all_tickers)

        self.graph_widget = pg.GraphicsLayoutWidget()
        self.gridLayout_2.addWidget(self.graph_widget)

        self.load_data(ticker)
        self.set_style_sheet()

        self.setWindowTitle(self.title)


    def load_data(self, ticker):
        start_date = "2019-01-01"
        self.data = sf.get_data(ticker, start_date=start_date, interval="1d")
        self.title = sf.get_earnings_history(ticker)[0]["companyshortname"]
        self.close_prices = self.data['close'].values
        self.date = [x.timestamp() for x in self.data.index]

        self.set_charts()
        # self.get_fondatamental(ticker)

    def get_fondatamental(self, ticker):
        # Clear Widget table
        busy = busy_indicator.BusyIndicator(parent=self)
        for i in reversed(range(self.verticalLayout.count())):
            self.verticalLayout.itemAt(i).widget().deleteLater()

        # busy.show()
        data = AnalyseFondamental(ticker)
        tablemodel = tableview.TableView(self, data.datas)
        self.verticalLayout.addWidget(tablemodel)
        # busy.hide()

    def set_charts(self):
        # Draw the quotations
        self.graph_widget.clear()
        self.draw_quotation()
        # Draw Candlestick
        # self.candlestick(self.data)
        self.draw_main_price()
        # Draw supports and resistances
        # self.draw_supports(closest=0.8)
        # self.draw_resistances(closest=0.8)
        # # # Draw Bollinger Bands
        # self.draw_bollinger_bands(self.data)
        # # # Draw Volume
        # self.draw_volume(values=self.data)
        # # Draw MVA (rolling mean)
        # self.draw_mva(data=self.data, lengths=[3, 5, 8, 10, 12, 15])
        # self.draw_mva(data=self.data, lengths=[20])
        # self.draw_mva(data=self.data, lengths=[200])
        # # # Draw ZigZag
        # self.draw_zig_zag()
        # # Draw RSI (Relative Strength Index)
        # self.draw_rsi()
        # # Draw MACD
        # self.draw_macd(self.data)

    def set_style_sheet(self):
        style = utils.load_stylesheet(os.path.dirname(__file__))
        self.setStyleSheet(style)
        color_backdround = (19, 23, 34)
        color = (14, 17, 25)
        pg.setConfigOption('background', color_backdround)

    def draw_quotation(self):
        self.quotation_graph = self.graph_widget.addPlot(row=0, col=0, name="Chart")
        self.quotation_graph.showGrid(x=True, y=True, alpha=0.3)

        self.range_view = (self.date[-240], self.date[-1])
        self.quotation_graph.setXRange(self.range_view[0], self.range_view[1])

        self.set_crosshaire_mouse()
        self.set_date_axis(self.quotation_graph)

        self.quotation_graph.showAxis('right')
        # self.quotation_graph.hideAxis('left')

        # Price
        self.quotation_graph.addLine(y=self.close_prices[-1],
                                     pen=pg.mkPen(color=(26, 100, 27),
                                     width=1,
                                     style=pg.QtCore.Qt.DashLine))

        axis = self.quotation_graph.getAxis('right')
        axis.setTicks([[(self.close_prices[-1], str(round(self.close_prices[-1], 2)))]])
        axis.setTextPen(pg.mkPen((26, 100, 27), width=3))
        self.label()

    def label(self):
        # Label Cursor
        self.price = pg.TextItem('exemple')
        self.price
        pg.GraphicsWidgetAnchor.__init__(self)
        self.quotation_graph.addItem(self.price, parent=self)

    def set_date_axis(self, item):
        axis = pg.DateAxisItem(orientation='bottom')
        item.setAxisItems({'bottom': axis})

    def set_crosshaire_mouse(self):
        # cross hair
        pen = pg.mkPen(color=(105, 105, 105), style=pg.QtCore.Qt.DashLine)
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pen)
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pen)
        self.quotation_graph.addItem(self.vLine, ignoreBounds=True)
        self.quotation_graph.addItem(self.hLine, ignoreBounds=True)

        self.crosshair_update = pg.SignalProxy(self.quotation_graph.scene().sigMouseMoved,
                                               rateLimit=60,
                                               slot=self.update_crosshair)

    def update_crosshair(self, event):
        """Paint crosshair on mouse"""
        mousePoint = self.quotation_graph.vb.mapSceneToView(event[0])
        self.vLine.setPos(mousePoint.x())
        self.hLine.setPos(mousePoint.y())
        # self.mouseMoved(event)

    def mouseMoved(self, evt):
        pos = evt[0]
        if self.quotation_graph.sceneBoundingRect().contains(pos):
            mousePoint = self.quotation_graph.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            print(index)
            # if index > 0 and index < len(data1):
                # label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>" % (
                #                 mousePoint.x(), data1[index]))

    # Charts

    def draw_main_price(self):
        self.quotation_graph.plot(x=self.date, y=self.close_prices, pen=pg.mkPen('w', width=3))

    def candlestick(self, data):
        """
        This function convert the Dataframe into a tuple:
        (index, Open, Close, High, Low)
        :param data:
        :return:
        """
        ls_data = []
        for index, i in enumerate(data.values):
            tuple_data = (self.date[index],
                          data['open'][index],
                          data['close'][index],
                          data['high'][index],
                          data['low'][index]
                          )
            ls_data.append(tuple_data)
        item = candlestick.CandlestickItem(ls_data)
        self.quotation_graph.addItem(item)

    def draw_mva(self, data, lengths=None):
        if not lengths or not self.quotation_graph:
            return

        for length in lengths:
            mva = self.data['close'].ewm(com=200).mean()
            # mva = indicators.moving_average(values=data['close'], w=length)
            self.quotation_graph.plot(
                x=self.date, y=mva,
                connect="finite",
                pen=pg.mkPen("b", width=1),
            )

    def draw_resistances(self, closest=None):
        if not self.quotation_graph:
            return

        resistances = indicators.get_resistances(
            values=self.close_prices, closest=closest
        )

        for res in resistances:
            self.quotation_graph.addLine(y=res, pen=pg.mkPen("r", width=1))

    def draw_supports(self, closest=None):
        if not self.quotation_graph:
            return

        supports = indicators.get_supports(values=self.close_prices, closest=closest)
        for sup in supports:
            self.quotation_graph.addLine(y=sup, pen=pg.mkPen("g", width=1))

    def draw_zig_zag(self):
        if not self.quotation_graph:
            return
        zigzag = indicators.zig_zag(values=self.data)
        self.quotation_graph.plot(x=self.date, y=zigzag['zigzag'], pen=pg.mkPen("g", width=1.2))

    def draw_bollinger_bands(self, values):
        color = (102, 169, 218, 0.3)
        middler, upper, lower = indicators.bollinger_bands(values)
        self.quotation_graph.plot(x=self.date, y=middler, pen=pg.mkPen(color=(color[0], color[1], color[2]), width=1.2))
        up = self.quotation_graph.plot(x=self.date, y=upper, pen=pg.mkPen(color=(color[0], color[1], color[2]), width=1.2))
        low = self.quotation_graph.plot(x=self.date, y=lower, pen=pg.mkPen(color=(color[0], color[1], color[2]), width=1.2))
        fill_bb = pg.FillBetweenItem(curve1=up, curve2=low, brush=pg.mkBrush(color[0], color[1], color[2], 50))
        self.quotation_graph.addItem(fill_bb)

    def draw_volume(self, values):
        volume_nrm = indicators.normalize(values)
        bar = BarGraph(x=self.date,
                       height=values['volume'].values,
                       width=1,
                       brush='r')
        self.volume_graph = self.graph_widget.addPlot(row=1, col=0)
        self.set_date_axis(self.volume_graph)
        self.volume_graph.addItem(bar)
        self.volume_graph.setMaximumHeight(150)
        self.volume_graph.setXLink("Chart")
        # pg.GraphicsScene.mouseEvents.HoverEvent()

    def draw_rsi(self, length=14):
        rsi = indicators.get_rsi(values=self.close_prices, length=length)
        self.rsi_graph = self.graph_widget.addPlot(row=2, col=0)
        self.set_date_axis(self.rsi_graph)
        self.rsi_graph.showGrid(x=True, y=True, alpha=1)
        self.rsi_graph.setMaximumHeight(150)
        self.rsi_graph.setXLink("Chart")

        self.rsi_graph.plot(x=self.date, y=rsi, connect="finite")
        self.rsi_graph.plot(
            x=self.date, y=indicators.savgol_filter(rsi, 51), pen=pg.mkPen("b", width=1)
        )

        # Draw overbought and oversold
        self.rsi_graph.addLine(x=self.date, y=70, pen=pg.mkPen("r", width=2))
        self.rsi_graph.addLine(x=self.date, y=30, pen=pg.mkPen("r", width=2))

    def draw_macd(self, data):
        self.macd_graph = self.graph_widget.addPlot(row=3, col=0)
        self.macd_graph.setXLink("Chart")
        self.set_date_axis(self.macd_graph)

        macd_line, signal_line, macd = indicators.macd(data['close'])
        ema9 = indicators.ExpMovingAverage(macd, w=9)
        macd_bar = macd - ema9

        # Histogram
        bars = BarGraph(x=range(macd.shape[0]),
                        height=macd_bar,
                        width=1,
                        brush='r')

        self.macd_graph.plot(x=self.date, y=ema9, pen=pg.mkPen('r', width=3))
        self.macd_graph.plot(x=self.date, y=macd, pen=pg.mkPen('b', width=3))
        self.macd_graph.addItem(bars)
        self.macd_graph.setMaximumHeight(150)
        self.macd_graph.showGrid(x=True, y=True, alpha=1)
        self.draw_macd_signal()

    def draw_macd_signal(self):
        x = stg.MACD_strategy(self.data)
        self.quotation_graph.plot(x=self.date, y=x['Buy'], pen=None, symbolBrush=(175, 0, 0), symbol='t', symbolSize=10, name="sell")
        self.quotation_graph.plot(x=self.date, y=x['Sell'], pen=None, symbolBrush=(0, 201, 80), symbol='t1', symbolSize=10, name="achat")


class TradingChart:
    def __init__(self, tick):
        super(TradingChart, self).__init__()
        app = QtWidgets.QApplication([])

        # All Markets Places
        try:
            with open(os.path.join(PATH, "dataset.json"), "r") as f:
                all_tickers = json.load(f)
        except:
            dow = sf.tickers_dow()
            cac = sf.tickers_cac()
            sp500 = sf.tickers_sp500()
            nasdaq = sf.tickers_nasdaq()
            all_tickers = {}
            for i in [cac, dow, nasdaq, sp500]:
                all_tickers.update(i)
            with open(os.path.join(PATH, "dataset.json"), "w") as outfile:
                json.dump(all_tickers, outfile)

        # Main Window
        main = GraphWindow(ticker=tick, all_tickers=all_tickers)

        # Show window
        stl.dark(app)
        mw = ws.ModernWindow(main)
        mw.show()
        app.exec_()


if __name__ == "__main__":
    tick = "BN.PA"
    chart = TradingChart(tick)
