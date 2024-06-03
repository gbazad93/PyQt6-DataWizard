import sys
import os
import pytest
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication

# Add the root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basic_data_handling import ApplicationWindow  
import io

@pytest.fixture(scope="session")
def app_instance():
    app = QApplication(sys.argv)
    return app

@pytest.fixture
def app_window(qtbot, app_instance, monkeypatch):
    # Create a mock pandas dataframe
    import pandas as pd
    from pandas._testing import makeMixedDataFrame
    df = makeMixedDataFrame()  # This creates a DataFrame with some test data

    # Mock the pandas read_csv method to return the test dataframe
    monkeypatch.setattr(pd, 'read_csv', lambda *args, **kwargs: df)
    
    # Mock the open method to return a fresh StringIO object each time it's called
    def mock_open(*args, **kwargs):
        return io.StringIO(df.to_csv(index=False))
    
    monkeypatch.setattr('builtins.open', mock_open)

    main_window = ApplicationWindow()
    qtbot.addWidget(main_window)
    return main_window

def test_initial_conditions(app_window, qtbot):
    """
    Test the initial state of the main window and its components.
    """
    # Check if the main window is set up properly
    assert app_window.ui.Label_Title.text() == "Data Analysis App, Version 1"
    # Since default data is loaded, the row count should not be 0
    assert app_window.ui.tableWidget.rowCount() > 0
    # The number of columns should also match the default data
    assert app_window.ui.tableWidget.columnCount() > 0

def test_csv_loading(app_window, qtbot, monkeypatch):
    """
    Test loading of CSV data into the table.
    """
    # Create a mock pandas dataframe
    import pandas as pd
    from pandas._testing import makeMixedDataFrame
    df = makeMixedDataFrame()  # This creates a DataFrame with some test data
    
    # Mock the pandas read_csv method to return the test dataframe
    monkeypatch.setattr(pd, 'read_csv', lambda *args, **kwargs: df)
    
    # Mock the open method to return a fresh StringIO object each time it's called
    def mock_open(*args, **kwargs):
        return io.StringIO(df.to_csv(index=False))
    
    monkeypatch.setattr('builtins.open', mock_open)

    # Trigger CSV loading
    app_window.read_csv_and_populate_table("dummy_path.csv")
    
    # Now, check if the data is loaded correctly into the table
    assert app_window.ui.tableWidget.rowCount() == len(df)
    assert app_window.ui.tableWidget.columnCount() == len(df.columns)
    for i in range(len(df)):
        for j in range(len(df.columns)):
            assert app_window.ui.tableWidget.item(i, j).text() == str(df.iloc[i, j])

def test_save_to_csv(app_window, qtbot, monkeypatch):
    """
    Test saving data from the table to a CSV file.
    """
    import pandas as pd
    monkeypatch.setattr(pd.DataFrame, 'to_csv', lambda self, file_path, index, header: print("Saved to CSV"))
    
    # Assume some data is already loaded into the table for simplicity
    qtbot.mouseClick(app_window.ui.saveButton, QtCore.Qt.MouseButton.LeftButton)
