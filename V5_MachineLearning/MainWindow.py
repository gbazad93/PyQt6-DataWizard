import io
import pandas as pd
import matplotlib.pyplot as plt
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon, QFont, QPixmap, QAction
from PyQt6.QtWidgets import (QGraphicsScene, QGraphicsPixmapItem, QMessageBox,
                             QFileDialog, QStyledItemDelegate, QLineEdit)
from PyQt6.QtCore import Qt

from MachineLearning import MachineLearningWindow


class CustomDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        if index.column() == 2:
            editor = QLineEdit(parent)
            return editor
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        if index.column() == 2:
            value = index.model().data(index, Qt.ItemDataRole.EditRole)
            editor.setText(str(value))
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if index.column() == 2:
            text = editor.text()
            try:
                value = float(text)
                model.setData(index, value, Qt.ItemDataRole.EditRole)
            except ValueError:
                QMessageBox.warning(editor, "Invalid Input",
                                    "Please enter a valid number.")
                return
        else:
            super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        if index.column() == 2:
            editor.setGeometry(option.rect)
        else:
            super().updateEditorGeometry(editor, option, index)


class MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 900)
        MainWindow.setWindowIcon(QIcon('../graphics/window_icon.png'))
        MainWindow.setMinimumSize(QtCore.QSize(1080, 900))
        MainWindow.setMaximumSize(QtCore.QSize(1080, 900))
        MainWindow.setStyleSheet("background-color: rgb(35, 35, 35);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.setupMenuBar(MainWindow)
        self.setupToolBar(MainWindow)
        self.setupWidgets()

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupWidgets(self):
        self.Label_Title = QtWidgets.QLabel(self.centralwidget)
        self.Label_Title.setGeometry(QtCore.QRect(450, 5, 300, 30))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Label_Title.setFont(font)
        self.Label_Title.setObjectName("Label_Title")
        self.Label_Title.setStyleSheet("color: rgb(255, 255, 255);")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 90, 620, 620))
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(630, 95, 435, 310))
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView2.setGeometry(QtCore.QRect(630, 410, 435, 310))
        self.graphicsView2.setObjectName("graphicsView2")

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(20, 760, 85, 35))
        self.saveButton.setObjectName("saveButton")

        self.saveAsButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveAsButton.setGeometry(QtCore.QRect(120, 760, 85, 35))
        self.saveAsButton.setObjectName("saveAsButton")

        self.plotButton = QtWidgets.QPushButton(self.centralwidget)
        self.plotButton.setGeometry(QtCore.QRect(220, 760, 85, 35))
        self.plotButton.setObjectName("plotButton")

        self.exportPlot1Button = QtWidgets.QPushButton(self.centralwidget)
        self.exportPlot1Button.setGeometry(QtCore.QRect(660, 750, 85, 35))
        self.exportPlot1Button.setObjectName("exportPlot1Button")

        self.exportPlot2Button = QtWidgets.QPushButton(self.centralwidget)
        self.exportPlot2Button.setGeometry(QtCore.QRect(770, 750, 85, 35))
        self.exportPlot2Button.setObjectName("exportPlot2Button")

        self.MachineLearningButton = QtWidgets.QPushButton(self.centralwidget)
        self.MachineLearningButton.setGeometry(QtCore.QRect(880, 750, 120, 35))
        self.MachineLearningButton.setObjectName("MachineLearningButton")

        button_color = "background-color: rgb(80, 150, 150); color: white;"
        self.saveButton.setStyleSheet(button_color)
        self.saveAsButton.setStyleSheet(button_color)
        self.plotButton.setStyleSheet(button_color)
        self.exportPlot1Button.setStyleSheet(button_color)
        self.exportPlot2Button.setStyleSheet(button_color)
        self.MachineLearningButton.setStyleSheet(button_color)

    def setupMenuBar(self, MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 22))
        MainWindow.setMenuBar(self.menubar)

        fileMenu = self.menubar.addMenu('&File')
        helpMenu = self.menubar.addMenu('&Help')

        openAction = QAction(
            QIcon('../graphics/open_icon.png'), '&Open', MainWindow)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open CSV File')
        openAction.triggered.connect(MainWindow.openFile)

        exitAction = QAction(
            QIcon('../graphics/exit_icon.png'), '&Exit', MainWindow)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(MainWindow.close)

        aboutAction = QAction(
            QIcon('../graphics/about_icon.png'), '&About', MainWindow)
        aboutAction.triggered.connect(self.aboutApp)

        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        helpMenu.addAction(aboutAction)

    def setupToolBar(self, MainWindow):
        toolbar = QtWidgets.QToolBar(MainWindow)
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, toolbar)
        toolbar.addAction(
            QAction(QIcon('../graphics/data_analysis.png'), 'Tool 1', MainWindow))
        toolbar.addAction(
            QAction(QIcon('../graphics/machine_learning.png'), 'Tool 2', MainWindow))
        toolbar.addAction(
            QAction(QIcon('../graphics/reporting.png'), 'Tool 3', MainWindow))

    def aboutApp(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("About Application")
        msgBox.setText(
            "PyQt6-DataWizard\nVersion 4: Learn about integrating advanced UI elements like Menus, Toolbars, and value validation.")

        windowIcon = QIcon('../graphics/window_icon.png')
        msgBox.setWindowIcon(windowIcon)

        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Data Analysis App"))
        self.Label_Title.setText(_translate(
            "MainWindow", "Data Analysis App, Version 5"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.saveAsButton.setText(_translate("MainWindow", "Save as"))
        self.plotButton.setText(_translate("MainWindow", "Plot"))
        self.exportPlot1Button.setText(
            _translate("MainWindow", "Export Plot1"))
        self.exportPlot2Button.setText(
            _translate("MainWindow", "Export Plot2"))
        self.MachineLearningButton.setText(
            _translate("MainWindow", "Machine Learning"))


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.read_csv_and_populate_table('data.csv')
        self.style_table()

        self.ui.tableWidget.setItemDelegateForColumn(
            2, CustomDelegate(self.ui.tableWidget))

        self.ui.saveButton.clicked.connect(
            lambda: self.save_table_to_csv('data.csv'))
        self.ui.saveAsButton.clicked.connect(self.save_as_table_to_csv)
        self.ui.plotButton.clicked.connect(self.plot_graphs)
        self.ui.exportPlot1Button.clicked.connect(self.export_plot1)
        self.ui.exportPlot2Button.clicked.connect(self.export_plot2)
        self.ui.MachineLearningButton.clicked.connect(
            self.open_machine_learning_window)
        self.fig1 = None
        self.fig2 = None

    def read_csv_and_populate_table(self, file_path):
        with open(file_path, newline='', mode='r') as file:
            initial_data = pd.read_csv(file)
            headers = initial_data.columns.tolist()

        with open(file_path, newline='', mode='r') as file:
            data = pd.read_csv(file, header=None)
            data.columns = headers

            self.ui.tableWidget.setColumnCount(len(data.columns))
            self.ui.tableWidget.setRowCount(len(data.index))

            self.ui.tableWidget.setHorizontalHeaderLabels(headers)

            for i, row in data.iterrows():
                for j, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(i, j, item)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            None, "Open CSV File", "", "CSV Files (*.csv)")
        if fileName:
            self.read_csv_and_populate_table(fileName)

    def style_table(self):
        header = self.ui.tableWidget.horizontalHeader()
        header.setStyleSheet("background-color: rgb(65, 65, 65);")

        self.ui.tableWidget.setStyleSheet("QTableWidget {color: white;}")

        for row in range(self.ui.tableWidget.rowCount()):
            for col in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.item(row, col)
                if item is not None:
                    if row % 2 == 0:
                        item.setBackground(QtGui.QColor(60, 60, 60))
                    else:
                        item.setBackground(QtGui.QColor(40, 40, 40))

                    if row == 0:
                        item.setBackground(QtGui.QColor(120, 120, 120))

    def save_table_to_csv(self, file_path):
        row_count = self.ui.tableWidget.rowCount()
        column_count = self.ui.tableWidget.columnCount()

        data = []
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.ui.tableWidget.item(row, column)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, header=[
                  self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count)])

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Save Successful")
        msg.setText("The data has been successfully saved!")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.exec()

    def save_as_table_to_csv(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File", "", "CSV Files (*.csv)")
        if path:
            self.save_table_to_csv(path)

    def get_table_data(self):
        row_count = self.ui.tableWidget.rowCount()
        column_count = self.ui.tableWidget.columnCount()
        table_data = []

        # Gather table data
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.ui.tableWidget.item(row, column)
                row_data.append(item.text() if item else "")
            table_data.append(row_data)

        # Get headers from the table
        headers = [self.ui.tableWidget.horizontalHeaderItem(
            i).text() for i in range(column_count)]

        # Create DataFrame
        df = pd.DataFrame(table_data, columns=headers)

        # Check if the first row is identical to the headers
        if df.iloc[0].equals(pd.Series(headers)):
            df = df.drop(0).reset_index(drop=True)

        return df

    def plot_graphs(self):
        df = self.get_table_data()

        df['Rainfall_mm'] = pd.to_numeric(df['Rainfall_mm'], errors='coerce')
        df['Yield_bushels_per_ac'] = pd.to_numeric(
            df['Yield_bushels_per_ac'], errors='coerce')

        df = df[df['Zone'] != 'Zone']

        color_map = ['green', 'lightgreen', 'yellow', 'orange', 'red']

        avg_rain = df.groupby('Zone')['Rainfall_mm'].mean()
        std_rain = df.groupby('Zone')['Rainfall_mm'].std()
        self.fig1, ax1 = plt.subplots()
        avg_rain.plot(kind='bar', ax=ax1, yerr=std_rain,
                      color=color_map, capsize=4)
        ax1.set_title('Average Rain Fall by Zone')
        ax1.set_xlabel('Zone')
        ax1.set_ylabel('Average Rain Fall')
        self.fig1.tight_layout()

        buf1 = io.BytesIO()
        self.fig1.savefig(buf1, format='png')
        buf1.seek(0)
        pixmap1 = QPixmap()
        pixmap1.loadFromData(buf1.getvalue())
        scene1 = QGraphicsScene()
        scene1.addItem(QGraphicsPixmapItem(pixmap1))
        self.ui.graphicsView.setScene(scene1)

        avg_yield = df.groupby('Zone')['Yield_bushels_per_ac'].mean()
        std_yield = df.groupby('Zone')['Yield_bushels_per_ac'].std()
        self.fig2, ax2 = plt.subplots()
        avg_yield.plot(kind='bar', ax=ax2, yerr=std_yield,
                       color=color_map, capsize=4)
        ax2.set_title('Average Yield by Zone')
        ax2.set_xlabel('Zone')
        ax2.set_ylabel('Average Yield')
        self.fig2.tight_layout()

        buf2 = io.BytesIO()
        self.fig2.savefig(buf2, format='png')
        buf2.seek(0)
        pixmap2 = QPixmap()
        pixmap2.loadFromData(buf2.getvalue())
        scene2 = QGraphicsScene()
        scene2.addItem(QGraphicsPixmapItem(pixmap2))
        self.ui.graphicsView2.setScene(scene2)

    def export_plot1(self):
        if self.fig1:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save Plot 1", "", "PNG Files (*.png)")
            if path:
                self.fig1.savefig(path, format='png')
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Export Successful")
                msg.setText("Plot 1 has been successfully exported!")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.exec()

    def export_plot2(self):
        if self.fig2:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "Save Plot 2", "", "PNG Files (*.png)")
            if path:
                self.fig2.savefig(path, format='png')
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Export Successful")
                msg.setText("Plot 2 has been successfully exported!")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.exec()

    def open_machine_learning_window(self):
        self.ml_window = MachineLearningWindow()
        self.ml_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ApplicationWindow()
    mainWindow.show()
    sys.exit(app.exec())
