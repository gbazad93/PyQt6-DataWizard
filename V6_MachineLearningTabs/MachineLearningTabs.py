# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 20:10:35 2024

@author: Bobby.Azad
"""

import sys
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVR
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt
import seaborn as sns
import io

from PyQt6 import (
    QtCore,
    QtGui,
    QtWidgets
)

from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsPixmapItem
)
from PyQt6.QtGui import QPixmap


class MachineLearningWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.svr = None
        self.init_ui()
        self.read_and_preprocess_data('data.csv')

    def init_ui(self):
        self.setWindowTitle("MachineLearningWindow")
        self.resize(1169, 892)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 1169, 892))

        self.tab1 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab1, "SVR")

        self.tab2 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab2, "DT/ RF/ K-NN Models")

        self.tab3 = QtWidgets.QWidget()
        self.tab_widget.addTab(self.tab3, "Extra Model")

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()
        self.setup_menu_and_status_bar()
        self.retranslate_ui()

        self.horizontalSlider.valueChanged.connect(self.update_label_display)
        self.update_label_display()

        self.trainButton.clicked.connect(self.train_model)
        self.testButton.clicked.connect(self.test_model)

    def setup_tab1(self):
        self.setup_graphics_views(self.tab1)
        self.setup_combo_box(self.tab1)
        self.setup_labels(self.tab1)
        self.setup_sliders(self.tab1)
        self.setup_spin_boxes(self.tab1)
        self.setup_buttons(self.tab1)

    def setup_graphics_views(self, parent):
        self.graphicsView = QtWidgets.QGraphicsView(parent)
        self.graphicsView.setGeometry(QtCore.QRect(20, 310, 561, 461))

        self.graphicsView2 = QtWidgets.QGraphicsView(parent)
        self.graphicsView2.setGeometry(QtCore.QRect(590, 310, 561, 461))

    def setup_combo_box(self, parent):
        self.comboBox = QtWidgets.QComboBox(parent)
        self.comboBox.setGeometry(QtCore.QRect(20, 200, 131, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.addItems(["linear", "poly", "rbf", "sigmoid"])

    def setup_labels(self, parent):
        font_bold = QtGui.QFont()
        font_bold.setPointSize(10)
        font_bold.setBold(True)

        self.label_kernelCombo = QtWidgets.QLabel(parent)
        self.label_kernelCombo.setGeometry(QtCore.QRect(20, 170, 101, 21))
        self.label_kernelCombo.setFont(font_bold)

        self.label_trainTestRatio = QtWidgets.QLabel(parent)
        self.label_trainTestRatio.setGeometry(QtCore.QRect(20, 40, 151, 21))
        self.label_trainTestRatio.setFont(font_bold)

        self.labelDisplay = QtWidgets.QLabel(parent)
        self.labelDisplay.setGeometry(QtCore.QRect(40, 80, 161, 20))
        font_normal = QtGui.QFont()
        font_normal.setPointSize(9)
        self.labelDisplay.setFont(font_normal)

        self.label_gammaSpinBox = QtWidgets.QLabel(parent)
        self.label_gammaSpinBox.setGeometry(QtCore.QRect(420, 60, 151, 21))
        self.label_gammaSpinBox.setFont(font_bold)

        self.label_epsilonSpinBox = QtWidgets.QLabel(parent)
        self.label_epsilonSpinBox.setGeometry(QtCore.QRect(420, 160, 151, 21))
        self.label_epsilonSpinBox.setFont(font_bold)

    def setup_sliders(self, parent):
        self.horizontalSlider = QtWidgets.QSlider(parent)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 100, 181, 22))
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)

    def setup_spin_boxes(self, parent):
        self.gammaSpinBox = QtWidgets.QDoubleSpinBox(parent)
        self.gammaSpinBox.setGeometry(QtCore.QRect(420, 90, 121, 22))
        self.gammaSpinBox.setMinimum(0.0)
        self.gammaSpinBox.setMaximum(1.0)
        self.gammaSpinBox.setSingleStep(0.001)
        self.gammaSpinBox.setValue(0.1)

        self.gammaSpinBox_2 = QtWidgets.QDoubleSpinBox(parent)
        self.gammaSpinBox_2.setGeometry(QtCore.QRect(420, 190, 121, 22))
        self.gammaSpinBox_2.setMinimum(0.0)
        self.gammaSpinBox_2.setMaximum(1.0)
        self.gammaSpinBox_2.setSingleStep(0.001)
        self.gammaSpinBox_2.setValue(0.1)

    def setup_buttons(self, parent):
        font_bold = QtGui.QFont()
        font_bold.setPointSize(9)
        font_bold.setBold(True)

        self.trainButton = QtWidgets.QPushButton(parent)
        self.trainButton.setGeometry(QtCore.QRect(950, 790, 81, 51))
        self.trainButton.setFont(font_bold)

        self.testButton = QtWidgets.QPushButton(parent)
        self.testButton.setGeometry(QtCore.QRect(1050, 790, 81, 51))
        self.testButton.setFont(font_bold)

    def setup_tab2(self):
        layout = QtWidgets.QVBoxLayout(self.tab2)

        self.second_model_label = QtWidgets.QLabel("Choose Model Parameters:")
        font_bold = QtGui.QFont()
        font_bold.setPointSize(12)
        font_bold.setBold(True)
        self.second_model_label.setFont(font_bold)
        layout.addWidget(self.second_model_label)

        self.model_combo_box = QtWidgets.QComboBox(self.tab2)
        self.model_combo_box.addItems(
            ["Decision Tree", "Random Forest", "K-Nearest Neighbors"])
        layout.addWidget(self.model_combo_box)

        self.param_label1 = QtWidgets.QLabel(
            "Parameter 1 (max_depth / n_estimators / n_neighbors):")
        layout.addWidget(self.param_label1)
        self.param_spin_box1 = QtWidgets.QSpinBox(self.tab2)
        self.param_spin_box1.setRange(1, 100)
        layout.addWidget(self.param_spin_box1)

        self.param_label2 = QtWidgets.QLabel(
            "Parameter 2 (min_samples_split / max_depth):")
        layout.addWidget(self.param_label2)
        self.param_spin_box2 = QtWidgets.QSpinBox(self.tab2)
        self.param_spin_box2.setRange(2, 100)
        layout.addWidget(self.param_spin_box2)

        self.train_button2 = QtWidgets.QPushButton(
            "Train Second Model", self.tab2)
        layout.addWidget(self.train_button2)

        self.graphics_view3 = QtWidgets.QGraphicsView(self.tab2)
        layout.addWidget(self.graphics_view3)

        self.train_button2.clicked.connect(self.train_second_model)

    def setup_tab3(self):
        """
        Use this method to setup third tab if needed.
        """
        pass

    def setup_menu_and_status_bar(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate(
            "MachineLearningWindow", "Machine Learning"))
        self.label_kernelCombo.setText(_translate(
            "MachineLearningWindow", "Kernel Type:"))
        self.label_trainTestRatio.setText(_translate(
            "MachineLearningWindow", "Train/Test Data Ratio:"))
        self.label_gammaSpinBox.setText(_translate(
            "MachineLearningWindow", "Gamma Parameter:"))
        self.label_epsilonSpinBox.setText(_translate(
            "MachineLearningWindow", "Epsilon Parameter:"))
        self.trainButton.setText(_translate("MachineLearningWindow", "Train"))
        self.testButton.setText(_translate("MachineLearningWindow", "Test"))

    def update_label_display(self):
        slider_value = self.horizontalSlider.value()
        test_ratio = slider_value
        train_ratio = 100 - slider_value
        self.labelDisplay.setText(
            f"Train: {train_ratio}%, Test: {test_ratio}%")

    def read_and_preprocess_data(self, file_path):
        self.data = pd.read_csv(file_path)
        self.data = self.data.dropna()
        self.data['Yield_bushels_per_ac'] = pd.to_numeric(
            self.data['Yield_bushels_per_ac'], errors='coerce')

        if self.data['Yield_bushels_per_ac'].isna().any():
            print("NaN values found in target column after conversion.")
            self.data = self.data.dropna(subset=['Yield_bushels_per_ac'])

        self.features = self.data.drop('Yield_bushels_per_ac', axis=1)
        self.target = self.data['Yield_bushels_per_ac']
        self.features['Zone'] = self.features['Zone'].astype(str)

        numeric_features = self.features.select_dtypes(
            include=['int64', 'float64']).columns
        categorical_features = self.features.select_dtypes(
            include=['object', 'category']).columns

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(), categorical_features)
            ])

        self.features_processed = preprocessor.fit_transform(self.features)

    def train_model(self):
        if self.data is None:
            QtWidgets.QMessageBox.warning(
                self, "No Data", "No data available for training.")
            return

        slider_value = self.horizontalSlider.value()
        test_size = slider_value / 100.0
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features_processed, self.target, test_size=test_size, random_state=42)

        if pd.isna(self.y_train).any() or pd.isna(self.y_test).any():
            QtWidgets.QMessageBox.warning(
                self, "NaN Values", "NaN values found in target sets after split.")
            return

        kernel = self.comboBox.currentText()
        gamma = self.gammaSpinBox.value()
        epsilon = self.gammaSpinBox_2.value()

        self.svr = SVR(kernel=kernel, gamma=gamma, epsilon=epsilon)
        self.svr.fit(self.X_train, self.y_train)

        self.plot_regression_results()

    def plot_regression_results(self):
        y_pred_train = self.svr.predict(self.X_train)
        y_pred_test = self.svr.predict(self.X_test)

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.scatterplot(x=self.y_test, y=y_pred_test, ax=ax,
                        label='Test Data', color='blue')
        sns.scatterplot(x=self.y_train, y=y_pred_train, ax=ax,
                        label='Train Data', color='orange')
        ax.plot([self.y_test.min(), self.y_test.max()], [
                self.y_test.min(), self.y_test.max()], 'k--', lw=2, label='Identity Line')
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title('Actual vs. Predicted Values')
        ax.legend()

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.graphicsView.setScene(scene)

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.residplot(x=y_pred_test, y=self.y_test - y_pred_test,
                      lowess=True, ax=ax, color='red')
        ax.set_xlabel('Predicted Values')
        ax.set_ylabel('Residuals')
        ax.set_title('Residuals Plot')

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.graphicsView2.setScene(scene)

    def test_model(self):
        if self.data is None:
            QtWidgets.QMessageBox.warning(
                self, "No Data", "No data available for testing.")
            return

        y_pred_test = self.svr.predict(self.X_test)
        r2 = r2_score(self.y_test, y_pred_test)

        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Test Results")
        msg.setText(f"R2 Score: {r2:.2f}")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.exec()

    def train_second_model(self):
        if self.data is None:
            QtWidgets.QMessageBox.warning(
                self, "No Data", "No data available for training.")
            return

        model_choice = self.model_combo_box.currentText()
        param1 = self.param_spin_box1.value()
        param2 = self.param_spin_box2.value()

        # Example: Decision Tree
        if model_choice == "Decision Tree":
            from sklearn.tree import DecisionTreeRegressor
            model = DecisionTreeRegressor(
                max_depth=param1, min_samples_split=param2)
        elif model_choice == "Random Forest":
            from sklearn.ensemble import RandomForestRegressor
            model = RandomForestRegressor(
                n_estimators=param1, max_depth=param2)
        elif model_choice == "K-Nearest Neighbors":
            from sklearn.neighbors import KNeighborsRegressor
            model = KNeighborsRegressor(n_neighbors=param1)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features_processed, self.target, test_size=0.2, random_state=42)

        model.fit(self.X_train, self.y_train)

        y_pred_train = model.predict(self.X_train)
        y_pred_test = model.predict(self.X_test)

        fig, ax = plt.subplots(figsize=(12, 8))
        sns.scatterplot(x=self.y_test, y=y_pred_test, ax=ax,
                        label='Test Data', color='blue')
        sns.scatterplot(x=self.y_train, y=y_pred_train, ax=ax,
                        label='Train Data', color='orange')
        ax.plot([self.y_test.min(), self.y_test.max()], [
                self.y_test.min(), self.y_test.max()], 'k--', lw=2, label='Identity Line')
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title(f'{model_choice}: Actual vs. Predicted Values')
        ax.legend()

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.graphics_view3.setScene(scene)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MachineLearningWindow()
    mainWindow.show()
    sys.exit(app.exec())
