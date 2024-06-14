# V4_DataValidation

## Overview
This version enhances the application by integrating selective data validation mechanisms. Using `QStyledItemDelegate`, it ensures that only numeric values are entered into designated columns of the table, maintaining data integrity while allowing flexibility for other data types in different columns.

## Features
This version introduces:
- **Selective Table Validation**: Implements custom delegates with `QStyledItemDelegate` to enforce numeric-only input for specific columns that require numeric data, while other columns can accept different types of data.
- **User Input Error Handling**: Provides immediate feedback for invalid entries in numeric columns, helping users correct data entry errors efficiently.


