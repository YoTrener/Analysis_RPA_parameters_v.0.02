# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidget, QMessageBox,
                             QTableWidgetItem, QHeaderView, QGridLayout, QInputDialog,
                             QVBoxLayout)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class VectorDiagramWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        # Добавьте нужные виджеты для второго окна сюда
        self.setLayout(layout)