# Version 5: Machine Learning Integration

## Overview

Version 5 introduces a dedicated Machine Learning Window alongside the main application window, significantly enhancing the application's functionality by incorporating a more complex dataset and machine learning capabilities. This version is designed to demonstrate how machine learning can be integrated into PyQt applications effectively.

## Dataset

The dataset used in this version is larger and more detailed, enabling us to perform meaningful machine learning analysis. It includes various features that influence crop yield, and our goal is to predict these yield outcomes based on input features. This setup provides a practical scenario for applying machine learning in agricultural data analysis.

## Machine Learning Algorithm

The core of this version is the implementation of the Support Vector Regression (SVR) algorithm. SVR is chosen for its effectiveness in handling non-linear data and its capability to perform regression tasks. Users can interact with the model through the following UI components:

- **Train and Test Data Size**: Users can specify the ratio of train to test data using a `horizontalSlider`, allowing for flexible dataset partitioning from 10% to 50% of the data reserved for testing.
- **Kernel Type**: A dropdown menu (`QComboBox`) lets users select the kernel type for the SVR algorithm, including options like linear, poly, rbf, and sigmoid.
- **Gamma and Epsilon Parameters**: These parameters are crucial for tuning the SVR model and can be adjusted via `QDoubleSpinBox` controls, providing precise control over the model's sensitivity and fitting behavior.

## Training and Testing the Model

Upon configuring the model parameters, users can initiate the training process by pressing the "Train" button. After training, the model can be tested with the designated test data. The results, including actual vs. predicted values and the residuals, are plotted in `QGraphicsView` panels, offering a visual assessment of the model's performance.

## Preprocessing Steps

Before feeding the data into the machine learning model, several preprocessing steps are automatically performed to ensure the data's suitability for analysis. These steps include scaling, handling missing values, and encoding categorical variables as necessary.

## Running the Application

To explore the machine learning features:
1. Run `MainWindow.py` to start the main application window.
2. Click on the "Machine Learning" button within the main window to launch the dedicated Machine Learning Window.

This modular approach allows users to interact with complex data and advanced analytics seamlessly within a user-friendly PyQt interface.
