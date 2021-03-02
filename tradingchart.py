# Yahoo Finance API
# https://algotrading101.com/learn/yahoo-finance-api-guide/

import os
from pprint import pprint

import talib
import pyqtgraph as pg
from PySide2 import QtWidgets
from yahoo_fin import stock_info as sf

import view

from utils import utils
from utils import tableview
from utils import indicators
from utils import candlestick
from utils.utils import BarGraph
from ui.qtmodern import windows as ws
from ui.qtmodern import styles as stl
from modules.analyse_financials import AnalyseFondamental


PATH = os.path.join(os.path.dirname(__file__), 'datas')

class GraphWindow(view.Window, QtWidgets.QMainWindow):
    def __init__(self, ticker, all_tickers):
        super(GraphWindow, self).__init__(ticker=ticker, all_tickers=all_tickers)

        self.load_data(ticker)

        offset = 50
        self.range_view = ((len(self.close_prices) - 365) + offset, len(self.close_prices) + offset)

        self.setWindowTitle(self.title)

        color_backdround = (19, 23, 34)
        color = (14, 17, 25)
        pg.setConfigOption('background', color_backdround)

        self.graph_widget = pg.GraphicsLayoutWidget()
        self.gridLayout_2.addWidget(self.graph_widget)

        self.quotation_graph = None
        self.rsi_graph = None

        self.draw_quotation()
        data = AnalyseFondamental(ticker)
        tablemodel = tableview.TableView(self, data.datas)
        self.verticalLayout.addWidget(tablemodel)

        self.set_style_sheet()

    def load_data(self, ticker):
        self.data = sf.get_data(ticker, start_date="2019-01-01", interval="1d")
        self.title = sf.get_earnings_history(ticker)[0]["companyshortname"]
        self.close_prices = self.data['close'].values

        self.date = []
        for x in self.data.index:
            self.date.append(x.strftime("%d/%m/%Y"))

    def set_charts(self):
        # Draw the quotations
        self.draw_quotation()
        # Draw Candlestick
        self.candlestick(self.data)
        self.draw_main_price()
        # # Draw supports and resistances
        self.draw_supports(closest=0.8)
        self.draw_resistances(closest=0.8)
        # # Draw Bollinger Bands
        self.draw_bollinger_bands(self.data)
        # # Draw Volume
        # main.draw_volume(values=data)
        # # Draw MVA (rolling mean)
        self.draw_mva(data=self.data, lengths=[3, 5, 8, 10, 12, 15])
        self.draw_mva(data=self.data, lengths=[20])
        # Draw ZigZag
        self.draw_zig_zag(value=self.close_prices)
        # Draw RSI (Relative Strength Index)
        # main.draw_rsi()
        # # Draw MACD
        # main.draw_macd(data)

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
        self.quotation_graph.plot(self.close_prices, pen=pg.mkPen('w', width=3))

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
        rsi = indicators.get_rsi(values=self.close_prices, length=length)
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


class TradingChart:
    def __init__(self, tick):
        super(TradingChart, self).__init__()
        app = QtWidgets.QApplication([])

        # All Markets Places
        dow = sf.tickers_dow()
        cac = sf.tickers_cac()
        sp500 = sf.tickers_sp500()
        nasdaq = sf.tickers_nasdaq()

        all_tickers = {}
        for i in [cac, dow, nasdaq, sp500]:
            all_tickers.update(i)

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