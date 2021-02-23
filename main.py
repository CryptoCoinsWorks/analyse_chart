# Yahoo Finance API
# https://algotrading101.com/learn/yahoo-finance-api-guide/

import os
import yfinance as yf
from pprint import pprint

from PySide2 import QtWidgets
import pyqtgraph as pg
import pandas as pd
import talib
from yahoo_fin import stock_info as sf

from ui import graphic_view
from utils.utils import BarGraph
from utils import indicators
from utils import candlestick
from utils import tableview
from utils import utils
from modules import launch
from modules.analyse_financials import AnalyseFondamental


PATH = os.path.join(os.path.dirname(__file__), 'datas')

class MainWindow(graphic_view.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, title, values, dates, ticker, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.values = values
        offset = 50
        self.range_view = ((len(self.values) - 365) + offset, len(self.values) + offset)
        self.date = []
        for i, x in enumerate(dates):
            self.date.append(x.strftime("%d/%m/%Y"))

        self.setWindowTitle(title)
        color_backdround = (19, 23, 34)
        color = (14, 17, 25)
        pg.setConfigOption('background', color_backdround)

        self.graph_widget = pg.GraphicsLayoutWidget()
        self.gridLayout_2.addWidget(self.graph_widget)

        self.quotation_graph = None
        self.rsi_graph = None

        data = AnalyseFondamental(ticker)
        # print(data.datas)
        # print(data.total_score())
        tablemodel = tableview.TableView(self, data.datas)
        self.verticalLayout.addWidget(tablemodel)

        self.set_style_sheet()

    def set_style_sheet(self):
        style = utils.load_stylesheet(os.path.dirname(__file__))
        self.setStyleSheet(style)

    def draw_quotation(self):
        self.quotation_graph = self.graph_widget.addPlot(row=0, col=0, name="Chart")
        self.quotation_graph.showGrid(x=True, y=True, alpha=0.3)
        # ax = self.quotation_graph.getAxis('bottom')
        # ax.tickStrings(self.date, 1, 1)
        # ax.setTicks([self.adjust_X_axis()])
        self.quotation_graph.setXRange(self.range_view[0], self.range_view[1])

    def adjust_X_axis(self):
        _pxLabelWidth = 80
        date = dict(enumerate(self.date)).items()
        return date

    def draw_main_price(self):
        self.quotation_graph.plot(self.values, pen=pg.mkPen('w', width=3))

    def candlestick(self, data):
        """
        This function convert the Dataframe into a tuple:
        (index, Open, Close, High, Low)
        :param data:
        :return:
        """
        ls_data = []
        for index, i in enumerate(data.values):
            tuple_data = (index,
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
            # mva = indicators.rolling_mean(values=self.values, length=length)
            mva = indicators.moving_average(values=data['close'], w=length)
            self.quotation_graph.plot(
                mva,
                connect="finite",
                pen=pg.mkPen("b", width=1),
            )

    def draw_resistances(self, closest=None):
        if not self.quotation_graph:
            return

        resistances = indicators.get_resistances(
            values=self.values, closest=closest
        )

        for res in resistances:
            self.quotation_graph.addLine(y=res, pen=pg.mkPen("r", width=1))

    def draw_supports(self, closest=None):
        if not self.quotation_graph:
            return

        supports = indicators.get_supports(values=self.values, closest=closest)
        for sup in supports:
            self.quotation_graph.addLine(y=sup, pen=pg.mkPen("g", width=1))

    def draw_zig_zag(self, value=None):
        if not self.quotation_graph:
            return

        zigzag = indicators.zig_zag(values=value)
        self.quotation_graph.plot(zigzag, value[zigzag], pen=pg.mkPen("g", width=1.2))

    def draw_bollinger_bands(self, values):
        color = (102, 169, 218, 0.3)
        middler, upper, lower = indicators.bollinger_bands(values)
        self.quotation_graph.plot(middler, pen=pg.mkPen(color=(color[0], color[1], color[2]), width=1.2))
        up = self.quotation_graph.plot(upper, pen=pg.mkPen(color=(color[0], color[1], color[2]), width=1.2))
        low = self.quotation_graph.plot(lower, pen=pg.mkPen(color=(color[0], color[1], color[2]), width=1.2))
        fill_bb = pg.FillBetweenItem(curve1=up, curve2=low, brush=pg.mkBrush(color[0], color[1], color[2], 50))
        self.quotation_graph.addItem(fill_bb)

    def draw_volume(self, values):
        volume_nrm = indicators.normalize(values)
        bar = BarGraph(x=range(volume_nrm.shape[0]),
                       height=values['volume'].values,
                       width=1,
                       brush='r')
        self.volume_graph = self.graph_widget.addPlot(row=1, col=0)
        self.volume_graph.addItem(bar)
        self.volume_graph.setMaximumHeight(150)
        self.volume_graph.setXLink("Chart")
        # pg.GraphicsScene.mouseEvents.HoverEvent()

    def draw_rsi(self, length=14):
        rsi = indicators.get_rsi(values=self.values, length=length)
        self.rsi_graph = self.graph_widget.addPlot(row=2, col=0)
        self.rsi_graph.showGrid(x=True, y=True, alpha=1)
        self.rsi_graph.setMaximumHeight(150)
        self.rsi_graph.setXLink("Chart")

        self.rsi_graph.plot(rsi, connect="finite")
        self.rsi_graph.plot(
            indicators.savgol_filter(rsi, 51), pen=pg.mkPen("b", width=1)
        )

        # Draw overbought and oversold
        self.rsi_graph.addLine(y=70, pen=pg.mkPen("r", width=2))
        self.rsi_graph.addLine(y=30, pen=pg.mkPen("r", width=2))

    def draw_macd(self, data):
        self.macd_graph = self.graph_widget.addPlot(row=3, col=0)
        self.macd_graph.setXLink("Chart")

        macd_line, signal_line, macd = indicators.macd(data['close'])
        ema9 = indicators.ExpMovingAverage(macd, w=9)
        macd_bar = macd - ema9

        # Histogram
        bars = BarGraph(x=range(macd.shape[0]),
                        height=macd_bar,
                        width=1,
                        brush='r')

        self.macd_graph.plot(ema9, pen=pg.mkPen('r', width=3))
        self.macd_graph.plot(macd, pen=pg.mkPen('b', width=3))
        self.macd_graph.addItem(bars)
        self.macd_graph.setMaximumHeight(150)
        self.macd_graph.showGrid(x=True, y=True, alpha=1)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    tick = "BN.PA"
    all_tickers = sf.tickers_other("CAC40")

    data = sf.get_data(tick, start_date="2019-01-01", interval="1d")

    # pprint(per)
    # pprint(income_statement)
    # pprint(balance)
    # pprint(cash_flow)

    title = sf.get_earnings_history(tick)[0]["companyshortname"]
    values = data['close'].values
    dates = data.index

    # Main Window
    main = MainWindow(title=title,
                      values=values,
                      dates=dates,
                      ticker=tick)
    # Draw the quotations
    main.draw_quotation()
    # Draw Candlestick
    # main.candlestick(data)
    main.draw_main_price()
    # # # Draw supports and resistances
    # main.draw_supports(closest=0.8)
    # main.draw_resistances(closest=0.8)
    # # # Draw Bollinger Bands
    # main.draw_bollinger_bands(data)
    # # # Draw Volume
    # main.draw_volume(values=data)
    # # # Draw MVA (rolling mean)
    # # # main.draw_mva(lengths=[3, 5, 8, 10, 12, 15])
    # main.draw_mva(data=data, lengths=[20])
    # # Draw ZigZag
    # main.draw_zig_zag(value=values)
    # # Draw RSI (Relative Strength Index)
    # main.draw_rsi()
    # # Draw MACD
    # main.draw_macd(data)

    # Show window
    main.show()
    app.exec_()
