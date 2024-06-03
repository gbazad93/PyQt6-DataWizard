"""
Created on Sat May 25 2024

@author: Bobby.Azad

"""

import io
import csv
import pandas as pd
import matplotlib.pyplot as plt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon,QFont, QColor, QPixmap
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem


class MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 848)
        MainWindow.setMinimumSize(QtCore.QSize(1080, 848))
        MainWindow.setMaximumSize(QtCore.QSize(1080, 848))
        MainWindow.setStyleSheet("background-color: rgb(35, 35, 35);")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.Label_Title = QtWidgets.QLabel(self.centralwidget)
        self.Label_Title.setGeometry(QtCore.QRect(450, 5, 300, 20))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)  
        self.Label_Title.setFont(font)
        self.Label_Title.setObjectName("Label_Title")
        self.Label_Title.setStyleSheet("color: rgb(255, 255, 255);")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 120, 620, 620))
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        # Disable grid lines)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.horizontalHeader().setVisible(False)  # Hides the horizontal header
        self.tableWidget.verticalHeader().setVisible(False)    # Hides the vertical header

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(630, 125, 435, 310))
        self.graphicsView.setObjectName("graphicsView")

        self.graphicsView2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView2.setGeometry(QtCore.QRect(630, 440, 435, 310))
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
        
        # Style buttons background color
        button_color = "background-color: rgb(80, 150, 150); color: white;"
        self.saveButton.setStyleSheet(button_color)
        self.saveAsButton.setStyleSheet(button_color)
        self.plotButton.setStyleSheet(button_color)
        self.exportPlot1Button.setStyleSheet(button_color)
        self.exportPlot2Button.setStyleSheet(button_color)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Analysis App"))
        self.Label_Title.setText(_translate("CornEditor", "Data Analysis App, Version 1"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.saveAsButton.setText(_translate("MainWindow", "Save as"))
        self.plotButton.setText(_translate("MainWindow", "Plot"))
        self.exportPlot1Button.setText(_translate("MainWindow", "Export Plot1"))
        self.exportPlot2Button.setText(_translate("MainWindow", "Export Plot2"))


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindow()
        self.ui.setupUi(self)
        self.read_csv_and_populate_table('data.csv')
        self.style_table()
        
        self.ui.saveButton.clicked.connect(lambda: self.save_table_to_csv('data.csv'))
        self.ui.saveAsButton.clicked.connect(self.save_as_table_to_csv)
        self.ui.plotButton.clicked.connect(self.plot_graphs)
        self.ui.exportPlot1Button.clicked.connect(self.export_plot1)
        self.ui.exportPlot2Button.clicked.connect(self.export_plot2)
        self.fig1 = None
        self.fig2 = None

    def read_csv_and_populate_table(self, file_path):
        # Read the CSV file to get headers (assuming the first row is headers)
        with open(file_path, newline='', mode='r') as file:
            initial_data = pd.read_csv(file)
            headers = initial_data.columns.tolist()  # Capture header names
            
        # Now reload the CSV treating everything as data
        with open(file_path, newline='', mode='r') as file:
            data = pd.read_csv(file, header=None)
            data.columns = headers  # Set the column names manually
        
            self.ui.tableWidget.setColumnCount(len(data.columns))
            self.ui.tableWidget.setRowCount(len(data.index))
            
            # Set headers for the table
            self.ui.tableWidget.setHorizontalHeaderLabels(headers)
            
            for i, row in data.iterrows():
                for j, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(i, j, item)
    



    def style_table(self):
        header = self.ui.tableWidget.horizontalHeader()
        header.setStyleSheet("background-color: rgb(65, 65, 65);")  # Lighter gray for the header for better contrast
    
        # Ensure consistent styling for all cells
        self.ui.tableWidget.setStyleSheet("QTableWidget {color: white;}")  # Set font color to white for all items
    
        for row in range(self.ui.tableWidget.rowCount()):
            for col in range(self.ui.tableWidget.columnCount()):
                item = self.ui.tableWidget.item(row, col)
                if item is not None:  # Check if the item is not None to avoid errors
                    if row % 2 == 0:
                        item.setBackground(QtGui.QColor(60, 60, 60))  # Slightly lighter gray for even rows
                    else:
                        item.setBackground(QtGui.QColor(40, 40, 40))  # Darker gray for odd rows

                    if row == 0:
                        item.setBackground(QtGui.QColor(120, 120, 120))


    def save_table_to_csv(self, file_path):
        # Number of rows and columns
        row_count = self.ui.tableWidget.rowCount()
        column_count = self.ui.tableWidget.columnCount()
    
        # Prepare data to save
        data = []
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.ui.tableWidget.item(row, column)
                row_data.append(item.text() if item else "")
            data.append(row_data)
    
        # Saving data to CSV
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, header=[self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count)])

        # Popup message
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Save Successful")
        msg.setText("The data has been successfully saved!")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.exec()


    def save_as_table_to_csv(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "CSV Files (*.csv)")
        if path:
            self.save_table_to_csv(path)

    def get_table_data(self):
        row_count = self.ui.tableWidget.rowCount()
        column_count = self.ui.tableWidget.columnCount()
        table_data = []

        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.ui.tableWidget.item(row, column)
                row_data.append(item.text() if item else "")
            table_data.append(row_data)

        headers = [self.ui.tableWidget.horizontalHeaderItem(i).text() for i in range(column_count)]
        return pd.DataFrame(table_data, columns=headers)

    def plot_graphs(self):
        # Get the data from the table
        df = self.get_table_data()
        
        # Convert columns to appropriate data types
        df['Protein'] = pd.to_numeric(df['Protein'], errors='coerce')
        df['Yield'] = pd.to_numeric(df['Yield'], errors='coerce')
        
        # Filter out the header row if it's included in the data
        df = df[df['Zone'] != 'Zone']

        # Define the color map
        color_map = ['green', 'lightgreen', 'yellow', 'orange', 'red']
        
        # First plot: Average protein content for each zone
        avg_protein = df.groupby('Zone')['Protein'].mean()
        std_protein = df.groupby('Zone')['Protein'].std()
        self.fig1, ax1 = plt.subplots()
        avg_protein.plot(kind='bar', ax=ax1, yerr=std_protein, color=color_map, capsize=4)
        ax1.set_title('Average Protein Content by Zone')
        ax1.set_xlabel('Zone')
        ax1.set_ylabel('Average Protein Content')
        self.fig1.tight_layout()

        # Convert the plot to a QPixmap and display it
        buf1 = io.BytesIO()
        self.fig1.savefig(buf1, format='png')
        buf1.seek(0)
        pixmap1 = QPixmap()
        pixmap1.loadFromData(buf1.getvalue())
        scene1 = QGraphicsScene()
        scene1.addItem(QGraphicsPixmapItem(pixmap1))
        self.ui.graphicsView.setScene(scene1)
        
        # Second plot: Average yield for each zone
        avg_yield = df.groupby('Zone')['Yield'].mean()
        std_yield = df.groupby('Zone')['Yield'].std()
        self.fig2, ax2 = plt.subplots()
        avg_yield.plot(kind='bar', ax=ax2, yerr=std_yield, color=color_map, capsize=4)
        ax2.set_title('Average Yield by Zone')
        ax2.set_xlabel('Zone')
        ax2.set_ylabel('Average Yield')
        self.fig2.tight_layout()

        # Convert the plot to a QPixmap and display it
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
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot 1", "", "PNG Files (*.png)")
            if path:
                self.fig1.savefig(path, format='png')
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Export Successful")
                msg.setText("Plot 1 has been successfully exported!")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.exec()

    def export_plot2(self):
        if self.fig2:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Plot 2", "", "PNG Files (*.png)")
            if path:
                self.fig2.savefig(path, format='png')
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Export Successful")
                msg.setText("Plot 2 has been successfully exported!")
                msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
                msg.exec()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ApplicationWindow()
    mainWindow.show()
    sys.exit(app.exec())

