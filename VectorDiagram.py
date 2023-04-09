# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class VectorDiagramWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.current_A_input = QLineEdit()
        self.current_B_input = QLineEdit()
        self.current_C_input = QLineEdit()
        self.angle_A_input = QLineEdit()
        self.angle_B_input = QLineEdit()
        self.angle_C_input = QLineEdit()

        form_layout.addRow(QLabel('Ток фазы, (А):'), self.current_A_input)
        form_layout.addRow(QLabel('Ток фазы, (А):'), self.current_B_input)
        form_layout.addRow(QLabel('Ток фазы, (А):'), self.current_C_input)
        form_layout.addRow(QLabel('Угол фазы A, (градусы):'), self.angle_A_input)
        form_layout.addRow(QLabel('Угол фазы B, (градусы):'), self.angle_B_input)
        form_layout.addRow(QLabel('Угол фазы C, (градусы):'), self.angle_C_input)

        plot_button = QPushButton('Построить график')
        plot_button.clicked.connect(self._plot_graph)
        form_layout.addRow(plot_button)

        clear_button = QPushButton('Очистить график')
        clear_button.clicked.connect(self._clear)
        form_layout.addRow(clear_button)

        layout.addLayout(form_layout)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def _plot_graph(self):
        currents = {'A': self.current_A_input, 'B': self.current_B_input, 'C': self.current_C_input}
        angles = {'A': self.angle_A_input, 'B': self.angle_B_input, 'C': self.angle_C_input}

        currents_complex = {}
        for key in currents:
            current = float(currents[key].text())
            angle = float(angles[key].text())
            angle_rad = np.deg2rad(angle)
            currents_complex[key] = current * (np.cos(angle_rad) + 1j * np.sin(angle_rad))

        self.figure.clf()
        ax = self.figure.add_subplot(1, 1, 1, projection='polar')

        colors = {'A': 'r', 'B': 'b', 'C': 'g'}
        for key in currents_complex:
            ax.quiver(0, 0, np.angle(currents_complex[key]), abs(currents_complex[key]),
                      angles='xy', scale_units='xy', scale=1, color=colors[key], label=f'I {key}')

        ax.set_ylim(0, max([abs(currents_complex[key]) for key in currents_complex]) * 1.2)
        ax.legend(loc='center left', bbox_to_anchor=(1.3, 0.5), borderaxespad=0.)
        ax.grid(alpha=0.8)

        self.canvas.draw()

    def _clear(self):
        # Отчистить график
        self.figure.clear()
        # Обновляем отображение графика на виджете
        self.canvas.draw()


