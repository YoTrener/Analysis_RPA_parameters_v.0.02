# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QWidget, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class VectorDiagramWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем разметку для виджета
        layout = QVBoxLayout()

        # Создаем форму для ввода значений токов и углов
        form_layout = QFormLayout()
        self.current_A_input = QLineEdit()
        self.current_B_input = QLineEdit()
        self.current_C_input = QLineEdit()
        self.angle_A_input = QLineEdit()
        self.angle_B_input = QLineEdit()
        self.angle_C_input = QLineEdit()

        # Добавляем поля для ввода токов и углов в форму
        form_layout.addRow(QLabel('Ток фазы, (А):'), self.current_A_input)
        form_layout.addRow(QLabel('Ток фазы, (А):'), self.current_B_input)
        form_layout.addRow(QLabel('Ток фазы, (А):'), self.current_C_input)
        form_layout.addRow(QLabel('Угол фазы A, (градусы):'), self.angle_A_input)
        form_layout.addRow(QLabel('Угол фазы B, (градусы):'), self.angle_B_input)
        form_layout.addRow(QLabel('Угол фазы C, (градусы):'), self.angle_C_input)

        # Создаем кнопку для построения графика и связываем ее с функцией _plot_graph
        plot_button = QPushButton('Построить график')
        plot_button.clicked.connect(self._plot)
        form_layout.addRow(plot_button)

        # Создаем кнопку для очистки графика и связываем ее с функцией _clear
        clear_button = QPushButton('Очистить график')
        clear_button.clicked.connect(self._clear)
        form_layout.addRow(clear_button)

        # Добавляем форму в основную разметку
        layout.addLayout(form_layout)

        # Создаем область для отображения графика
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Добавляем область графика и панель инструментов в основную разметку
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def _plot(self):
        # Считываем значения токов и углов из полей ввода
        currents = {'A': self.current_A_input, 'B': self.current_B_input, 'C': self.current_C_input}
        angles = {'A': self.angle_A_input, 'B': self.angle_B_input, 'C': self.angle_C_input}

        # Переводим значения токов и углов в комплексные токи
        currents_complex = {}
        for key in currents:
            current = float(currents[key].text())
            angle = float(angles[key].text())
            angle_rad = np.deg2rad(angle)
            currents_complex[key] = current * (np.cos(angle_rad) + 1j * np.sin(angle_rad))

        # Очищаем текущий график
        self.figure.clf()
        # Создаем новый полярный график
        ax = self.figure.add_subplot(1, 1, 1, projection='polar')

        # Рисуем векторы токов на графике
        colors = {'A': 'r', 'B': 'b', 'C': 'g'}
        for key in currents_complex:
            ax.quiver(0, 0, np.angle(currents_complex[key]), abs(currents_complex[key]),
                      angles='xy', scale_units='xy', scale=1, color=colors[key], label=f'I {key}')

        # Устанавливаем пределы для оси r и добавляем легенду
        ax.set_ylim(0, max([abs(currents_complex[key]) for key in currents_complex]) * 1.2)
        ax.legend(loc='center left', bbox_to_anchor=(1.3, 0.5), borderaxespad=0.)

        # Устанавливаем прозрачность сетки
        ax.grid(alpha=0.8)

        # Обновляем отображение графика на виджете
        self.canvas.draw()

    def _clear(self):
        # Отчистить график
        self.figure.clear()
        # Обновляем отображение графика на виджете
        self.canvas.draw()


