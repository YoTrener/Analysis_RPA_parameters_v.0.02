# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QMenuBar,
                             QMenu, QAction, QFileDialog)

from VoltAmpereCharacteristic import VoltAmpereCharacteristicWindow
from VectorDiagram import VectorDiagramWindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.file_menu = QMenu('Файл', self)
        self.menubar.addMenu(self.file_menu)

        self.action_save_to_excel = QAction('Сохранить в Excel')
        self.action_save_to_excel.triggered.connect(self.import_to_excel)
        self.file_menu.addAction(self.action_save_to_excel)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.first_window = VoltAmpereCharacteristicWindow()
        self.second_window = VectorDiagramWindow()

        self.tab_widget.addTab(self.first_window, 'Вольт-Амперная характеристика')
        self.tab_widget.addTab(self.second_window, 'Векторная диаграмма')

        self.setWindowTitle('Анализ параметров РЗА')
        self.setGeometry(100, 100, 950, 600)

    def import_to_excel(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить как', '', 'Excel Files (*.xlsx);;All Files (*)')
        if not file_name:
            return

        # Если имя файла не заканчивается на ".xlsx", добавляем это расширение
        if not file_name.endswith('.xlsx'):
            file_name += '.xlsx'

        # Получаем данные из таблицы VoltAmpereCharacteristicWindow
        df = self.first_window.get_table_data()
        # Сохраняем данные в Excel-файл
        df.to_excel(file_name, index=False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
