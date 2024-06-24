import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import io
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QMessageBox
from PyQt6.QtGui import QPixmap


class MachineLearningWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.read_and_preprocess_data('data.csv')

    def init_ui(self):
        self.setWindowTitle("MachineLearningWindow")
        self.resize(1169, 892)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.setup_graphics_views()
        self.setup_combo_box()
        self.setup_labels()
        self.setup_sliders()
        self.setup_spin_boxes()
        self.setup_buttons()
        self.setup_menu_and_status_bar()

        self.retranslate_ui()

        # Connect slider value change to the update method
        self.horizontalSlider.valueChanged.connect(self.update_label_display)

        # Initialize label with the slider's initial value
        self.update_label_display()

        # Connect the train button to the train method
        self.trainButton.clicked.connect(self.train_model)

        # Connect the test button to the test method
        self.testButton.clicked.connect(self.test_model)

    def setup_graphics_views(self):
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 310, 561, 461))

        self.graphicsView2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView2.setGeometry(QtCore.QRect(590, 310, 561, 461))

    def setup_combo_box(self):
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 200, 131, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.addItems(["linear", "poly", "rbf", "sigmoid"])

    def setup_labels(self):
        font_bold = QtGui.QFont()
        font_bold.setPointSize(10)
        font_bold.setBold(True)

        self.label_kernelCombo = QtWidgets.QLabel(self.centralwidget)
        self.label_kernelCombo.setGeometry(QtCore.QRect(20, 170, 101, 21))
        self.label_kernelCombo.setFont(font_bold)

        self.label_trainTestRatio = QtWidgets.QLabel(self.centralwidget)
        self.label_trainTestRatio.setGeometry(QtCore.QRect(20, 40, 151, 21))
        self.label_trainTestRatio.setFont(font_bold)

        self.labelDisplay = QtWidgets.QLabel(self.centralwidget)
        self.labelDisplay.setGeometry(QtCore.QRect(40, 80, 161, 20))
        font_normal = QtGui.QFont()
        font_normal.setPointSize(9)
        self.labelDisplay.setFont(font_normal)

        self.label_gammaSpinBox = QtWidgets.QLabel(self.centralwidget)
        self.label_gammaSpinBox.setGeometry(QtCore.QRect(420, 60, 151, 21))
        self.label_gammaSpinBox.setFont(font_bold)

        self.label_epsilonSpinBox = QtWidgets.QLabel(self.centralwidget)
        self.label_epsilonSpinBox.setGeometry(QtCore.QRect(420, 160, 151, 21))
        self.label_epsilonSpinBox.setFont(font_bold)

    def setup_sliders(self):
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 100, 181, 22))
        self.horizontalSlider.setMinimum(10)
        self.horizontalSlider.setMaximum(50)
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)

    def setup_spin_boxes(self):
        self.gammaSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.gammaSpinBox.setGeometry(QtCore.QRect(420, 90, 121, 22))
        self.gammaSpinBox.setMinimum(0.0)
        self.gammaSpinBox.setMaximum(1.0)
        self.gammaSpinBox.setSingleStep(0.001)
        self.gammaSpinBox.setValue(0.1)

        self.gammaSpinBox_2 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.gammaSpinBox_2.setGeometry(QtCore.QRect(420, 190, 121, 22))
        self.gammaSpinBox_2.setMinimum(0.0)
        self.gammaSpinBox_2.setMaximum(1.0)
        self.gammaSpinBox_2.setSingleStep(0.001)
        self.gammaSpinBox_2.setValue(0.1)

    def setup_buttons(self):
        font_bold = QtGui.QFont()
        font_bold.setPointSize(9)
        font_bold.setBold(True)

        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(950, 790, 81, 51))
        self.trainButton.setFont(font_bold)

        self.testButton = QtWidgets.QPushButton(self.centralwidget)
        self.testButton.setGeometry(QtCore.QRect(1050, 790, 81, 51))
        self.testButton.setFont(font_bold)

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
        # Read the CSV file
        self.data = pd.read_csv(file_path)

        # Preprocessing steps
        self.data = self.data.dropna()

        # Ensure the target column is in numeric format
        self.data['Yield_bushels_per_ac'] = pd.to_numeric(
            self.data['Yield_bushels_per_ac'], errors='coerce')

        # Check for NaN values in the target variable
        if self.data['Yield_bushels_per_ac'].isna().any():
            print("NaN values found in target column after conversion.")
            self.data = self.data.dropna(subset=['Yield_bushels_per_ac'])

        # Extract features and target
        self.features = self.data.drop('Yield_bushels_per_ac', axis=1)
        self.target = self.data['Yield_bushels_per_ac']

        # Convert 'Zone' to string to handle it as a categorical variable
        self.features['Zone'] = self.features['Zone'].astype(str)

        # One-hot encode categorical features and scale numeric features
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

        # Splitting the data
        slider_value = self.horizontalSlider.value()
        test_size = slider_value / 100.0
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features_processed, self.target, test_size=test_size, random_state=42)

        # Ensure there are no NaN values in the target sets
        if pd.isna(self.y_train).any() or pd.isna(self.y_test).any():
            QtWidgets.QMessageBox.warning(
                self, "NaN Values", "NaN values found in target sets after split.")
            return

        # Read parameters from the UI
        kernel = self.comboBox.currentText()
        gamma = self.gammaSpinBox.value()
        epsilon = self.gammaSpinBox_2.value()

        # Train the model
        self.svr = SVR(kernel=kernel, gamma=gamma, epsilon=epsilon)
        self.svr.fit(self.X_train, self.y_train)

        # Plotting the results
        self.plot_regression_results()

    def plot_regression_results(self):
        y_pred_train = self.svr.predict(self.X_train)
        y_pred_test = self.svr.predict(self.X_test)

        # Create a joint plot with seaborn
        fig, ax = plt.subplots(figsize=(8, 5))

        sns.scatterplot(x=self.y_test, y=y_pred_test, ax=ax,
                        label='Test Data', color='blue')
        sns.scatterplot(x=self.y_train, y=y_pred_train, ax=ax,
                        label='Train Data', color='orange')

        # Plot the identity line (where predicted values equal actual values)
        ax.plot([self.y_test.min(), self.y_test.max()], [
                self.y_test.min(), self.y_test.max()], 'k--', lw=2, label='Identity Line')

        # Labels, title, and legend
        ax.set_xlabel('Actual Values')
        ax.set_ylabel('Predicted Values')
        ax.set_title('Actual vs. Predicted Values')
        ax.legend()

        # Save the plot to a buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        # Convert the buffer to a QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        # Display the pixmap in the QGraphicsView
        scene = QGraphicsScene()
        scene.addItem(QGraphicsPixmapItem(pixmap))
        self.graphicsView.setScene(scene)

        # Residual plot
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.residplot(x=y_pred_test, y=self.y_test - y_pred_test,
                      lowess=True, ax=ax, color='red')

        # Labels, title, and legend
        ax.set_xlabel('Predicted Values')
        ax.set_ylabel('Residuals')
        ax.set_title('Residuals Plot')

        # Save the plot to a buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        # Convert the buffer to a QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        # Display the pixmap in the QGraphicsView
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MachineLearningWindow()
    mainWindow.show()
    sys.exit(app.exec())
