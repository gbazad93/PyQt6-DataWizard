# Version 6: Multi Tab MachineLearning Window

## Overview

In this version, we a tabbed interface integrated that allows users to perform different machine learning algorithms within the same application. Each tab provides a dedicated environment to configure, train, and evaluate specific machine learning models. This version builds upon the previous implementation, adding a more organized and user-friendly interface for machine learning tasks.

## Features

- **Tabbed Interface**: Users can switch between tabs to use different machine learning algorithms.
- **Machine Learning Algorithms**: Support for multiple machine learning models.
- **Configurable Parameters**: Each tab allows users to set parameters specific to the algorithm.
- **Training and Testing**: Users can train and test models directly from the UI.
- **Visualization**: Each tab includes plots for visualizing model performance and residuals.
- **Data Management**: Easily load and manage datasets for machine learning.

## Machine Learning Algorithms

**Tab 1: Support Vector Regression (SVR)**
- Train/Test Data Ratio: Adjust the ratio using a horizontal slider to allocate data for training and testing.
- Kernel Type: Select the kernel type from a dropdown menu.
- Gamma and Epsilon: Set these parameters using QDoubleSpinBox inputs.
- Visualizations: Actual vs. predicted values and residuals are plotted in graphics views.
  
**Tab 2: Decision Tree, Random Forest, and K-NN**
- Model Selection: Choose between Decision Tree, Random Forest, and K-NN using a dropdown menu.
- Configurable Parameters: Set parameters specific to the chosen model.
- Visualizations: Actual vs. predicted values plot with blue dots for test data, orange dots for train data, and a dashed line for the identity line.
  
**Tab 3: Extra Model**
- Custom Tab: An empty tab labeled "Extra Model" is included for additional use cases. Users can add their own machine learning models and components by editing the setup_tab3 method in the source code.
