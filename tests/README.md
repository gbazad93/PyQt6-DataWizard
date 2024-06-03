# Tests Directory README

## Overview
This directory contains the unit tests for the PyQt6-DataWizard project. Unit tests are essential tools for ensuring that individual components of our application perform as expected. They help us identify bugs early in the development process, improve code quality, and ensure that new changes do not break existing functionality.

## Purpose of Unit Testing
Unit testing involves isolating individual parts (units) of the program to verify that each part works correctly on its own. This helps in:
- Detecting and fixing bugs early
- Facilitating changes and simplifying integration
- Providing documentation on what the code is supposed to do
- Ensuring that the system behaves as intended after changes or enhancements

## How to Run Tests
We use `pytest` for running unit tests due to its simplicity and powerful features. To execute the tests, make sure you have `pytest` installed, which can be done via pip:

```bash
pip install pytest
```

Bellow you can see the resulted output of unnit test for V1
```bash
platform win32 -- Python 3.11.7, pytest-7.4.0, pluggy-1.5.0
PyQt6 6.7.0 -- Qt runtime 6.7.0 -- Qt compiled 6.7.0
rootdir: C:\Users\Bobby\Desktop\PyQt6 Prj
plugins: anyio-4.2.0, qt-4.4.0
collected 3 items

test_V1_basicDataHandling.py ...                                                                                 [100%]

================================================== 3 passed in 2.35s ==================================================
```


