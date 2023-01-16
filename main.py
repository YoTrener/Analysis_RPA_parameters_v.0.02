# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from mywindow import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ui.chartWidget.addWidget(self.toolbar)
        self.ui.chartWidget.addWidget(self.canvas)
        self.ui.pushButton.clicked.connect(self.plot) # Подключаем кнопку к построению графика

    # Получаем значения, введенные в таблицу пользователем
    def getData(self):
        rows = self.ui.tableWidget.rowCount()
        cols = self.ui.tableWidget.columnCount()
        table_data = []
        for i_row in range(rows):
            tmp = []
            for i_col in range(cols):
                try:
                    tmp.append(self.ui.tableWidget.item(i_row, i_col).text().replace(',', '.'))
                except:
                    tmp.append('No Data')
            table_data.append(tmp)
        return table_data

    # Метод для создания графика на основании полученных значений от пользователя
    def plot(self):
        table_list = self.getData()
        data_dict = {}
        for i in table_list:
            data_dict[i[0]] = i[1:]
        df = pd.DataFrame(data=data_dict, index=['0.5', '10P'], dtype='float64').transpose()
        sns.lineplot(df, markers=True)
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
application = Window()
application.show()

sys.exit(app.exec_())