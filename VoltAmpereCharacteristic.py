# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QWidget, QPushButton, QTableWidget, QMessageBox,
                             QTableWidgetItem, QHeaderView, QGridLayout, QInputDialog)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class VoltAmpereCharacteristicWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Задаем начальные значения тока
        current = [0, 0.2, 0.4, 0.6, 0.8, 1, 2, 3, 4, 5]

        # Создаем виджет таблицы для ввода данных и настраиваем его
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(9)  # Устанавливаем количество строк таблицы (9)
        self.table_widget.setColumnCount(1)  # Устанавливаем количество столбцов таблицы (1)
        self.table_widget.setHorizontalHeaderLabels(['Ток, А'])  # Устанавливаем заголовок для первого столбца
        self.table_widget.horizontalHeader()\
            .setSectionResizeMode(QHeaderView.Stretch)  # Растягиваем столбцы на всю ширину таблицы

        # Заполняем первый столбец значениями тока
        for row, i_current in enumerate(current):
            item = QTableWidgetItem(str(i_current))
            self.table_widget.setItem(row, 0, item)

        # Создаем объекты для отображения графика и добавляем их на виджет
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Создаем кнопки и связываем их с соответствующими функциями
        self.build_button = QPushButton('Построить график')
        self.build_button.clicked.connect(self.plot)

        self.add_column_button = QPushButton('Добавить столбец')
        self.add_column_button.clicked.connect(self._add_column)

        self.remove_column_button = QPushButton('Удалить столбец')
        self.remove_column_button.clicked.connect(self._remove_column)

        self.clear_button = QPushButton('Очистить график')
        self.clear_button.clicked.connect(self._clear)

        # Размещаем виджеты на сетке
        layout = QGridLayout()
        layout.addWidget(self.table_widget, 0, 0, 1, 2)  # Размещаем виджет таблицы
        layout.addWidget(self.build_button, 1, 0)  # Размещаем кнопку "Построить график"
        layout.addWidget(self.add_column_button, 1, 1)  # Размещаем кнопку "Добавить столбец"
        layout.addWidget(self.remove_column_button, 2, 1)  # Размещаем кнопку "Удалить столбец"
        layout.addWidget(self.clear_button, 2, 0)  # Размещаем кнопку "Очистить график"
        layout.addWidget(self.toolbar, 3, 2, 1, 2)  # Размещаем панель инструментов графика
        layout.addWidget(self.canvas, 0, 2, 3, 1)  # Размещаем область графика

        self.setLayout(layout)  # Применяем разметку к виджету

    def plot(self):
        df = self.get_table_data()

        if df.empty:
            # Если DataFrame пуст, показываем сообщение об ошибке
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Warning)
            error_dialog.setWindowTitle('Ошибка ввода')
            error_dialog.setText('Данные для построения графика отсутствуют.\nПожалуйста, введите данные.')
            error_dialog.exec()
            return

        # Очищаем текущий график
        plt.clf()
        # Строим график с помощью seaborn.lineplot с данными из DataFrame
        sns.lineplot(data=df, x='Ток, А', y='Напряжение', hue='Класс точности',
                     style='Класс точности', markers=True, dashes=False)
        # Отобразим сетку на графике
        plt.grid()
        # Обновляем отображение графика на виджете
        self.canvas.draw()

    def get_table_data(self):
        # Создаем пустой словарь для хранения данных из таблицы
        data = {}
        for row in range(self.table_widget.rowCount()):
            current_item = self.table_widget.item(row, 0)  # Получаем элемент текущей строки из столбца с токами
            if current_item:  # Проверяем, что элемент существует
                current_item = float(current_item.text())  # Конвертируем текст элемента в число с плавающей точкой
                # Итерируемся по столбцам таблицы, начиная со второго
                for col in range(1, self.table_widget.columnCount()):
                    voltage_item = self.table_widget.item(row, col)  # Получаем элемент текущей строки и столбца
                    if voltage_item:  # Проверяем, что элемент существует
                        voltage_item = float(voltage_item.text().replace(',', '.'))  # Конвертируем текст элемента в
                        # число с плавающей точкой и заменяем запятую на точку
                        column_name = self.table_widget.horizontalHeaderItem(col) \
                            .text()  # Получаем имя текущего столбца
                        # Если имя столбца еще не добавлено в словарь, добавляем его
                        if column_name not in data:
                            data[column_name] = []
                        # Добавляем пару (ток, напряжение) в список для текущего столбца
                        data[column_name].append((current_item, voltage_item))

        # Создаем пустой список для хранения данных, которые будут переданы в DataFrame
        df_list = []
        # Итерируемся по категориям и точкам словаря data
        for category, points in data.items():
            for current, voltage in points:
                # Добавляем словарь с данными для каждой точки в список df_list
                df_list.append({'Ток, А': current, 'Напряжение': voltage, 'Класс точности': category})

        # Создаем DataFrame на основе списка df_list
        return pd.DataFrame(df_list)

    def _add_column(self):
        # Получаем текущее количество столбцов в таблице
        current_column_count = self.table_widget.columnCount()

        # Открываем диалоговое окно для ввода наименования нового столбца
        column_name, ok_pressed = QInputDialog.getText(self, 'Введите наименование столбца', 'Наименование столбца:')
        # Если пользователь нажал кнопку "OK" и ввел имя столбца
        if ok_pressed and column_name:
            # Устанавливаем новое количество столбцов, увеличивая текущее значение на 1
            self.table_widget.setColumnCount(current_column_count + 1)
            # Устанавливаем имя нового столбца в горизонтальном заголовке таблицы
            self.table_widget.setHorizontalHeaderItem(current_column_count, QTableWidgetItem(column_name))

    def _remove_column(self):
        # Получаем текущее количество столбцов в таблице
        current_column_count = self.table_widget.columnCount()
        # Удаляем столбец
        self.table_widget.setColumnCount(current_column_count - 1)

    def _clear(self):
        # Отчистить график
        self.figure.clear()
        # Обновляем отображение графика на виджете
        self.canvas.draw()
