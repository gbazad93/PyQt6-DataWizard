"""
Created on Sat May 4 2024

@author: Bobby.Azad

"""


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon,QFont, QColor
import pandas as pd
import csv


class Ui_MainWindow:
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
        
        self.tableWidget.setShowGrid(False) # Disable grid lines)
        self.tableWidget.horizontalHeader().setVisible(False)  # Hides the horizontal header
        self.tableWidget.verticalHeader().setVisible(False)    # Hides the vertical header

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(20, 760, 85, 35))
        self.saveButton.setObjectName("saveButton")

        self.saveAsButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveAsButton.setGeometry(QtCore.QRect(120, 760, 85, 35))
        self.saveAsButton.setObjectName("saveAsButton")
        
        # Style buttons background color
        button_color = "background-color: rgb(80, 150, 150); color: white;"
        self.saveButton.setStyleSheet(button_color)
        self.saveAsButton.setStyleSheet(button_color)
        
        

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



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.read_csv_and_populate_table('data.csv')
        self.style_table()
        
        self.ui.saveButton.clicked.connect(lambda: self.save_table_to_csv('data.csv'))
        self.ui.saveAsButton.clicked.connect(self.save_as_table_to_csv)

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



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ApplicationWindow()
    mainWindow.show()
    sys.exit(app.exec())

