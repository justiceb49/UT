#!/bin/env/python

#Developed by Justice Boisselle 2017
# Import
import sys, os
from PyQt5.QtWidgets import (QMainWindow,
                             QWidget,
                             QFileDialog,
                             QLabel,
                             QCheckBox,
                             QVBoxLayout,
                             QApplication,
                             QPushButton,
                             QTableWidget,
                             QTableWidgetItem)
from PyQt5.QtCore import QCoreApplication

import numpy as np
from scipy import stats


class StatCalculator(QMainWindow):
    # The init function always runs upon instantiation
    def __init__(self):
        super().__init__()  # initializes the inherited class

        # Upon startup, run a user interface routine
        self.init_ui()

    def init_ui(self):
        # Builds GUI
        self.setGeometry(200, 200, 500, 500)

        self.load_button = QPushButton('Load Data', self)
        self.load_button.clicked.connect(self.load_data)

        self.mean_label = QLabel("Mean: Not Computed Yet", self)
        # add more labels here

        # Set up a Table to display data
        self.data_table = QTableWidget()
        # Connect the signal to the slot. IN other words, whenever the selection of the table changes, compute stats.
        self.data_table.itemSelectionChanged.connect(self.compute_stats)

        # Define where the widgets go in the window
        v_layout = QVBoxLayout()

        v_layout.addWidget(self.load_button)
        v_layout.addWidget(self.data_table)
        v_layout.addWidget(self.mean_label)
        # add more labels to the layout here

        main_widget.setLayout(v_layout)
        self.setCentralWidget(main_widget)

        self.setWindowTitle('Introduction to Descriptive Statistics')
        self.show()

    def load_data(self):
        # for this example, we'll hard code the file name.
        data_file_name = "Historical Temperatures from Moose Wyoming.csv"
        # for the assignment, have a dialog box provide the filename

        # check to see if the file exists and then load it
        if os.path.exists(data_file_name):
            header_row = 1
            # load data file into memory as a list of lines
            with open(data_file_name, 'r') as data_file:
                self.data_lines = data_file.readlines()

            print("Opened {}".format(data_file_name))
            print(self.data_lines[1:10])

            # Set the headers
            # parse the lines by stripping the newline character off the end
            # and then splitting them on commas.
            data_table_columns = self.data_lines[header_row].strip().split(',')
            self.data_table.setColumnCount(len(data_table_columns))
            self.data_table.setHorizontalHeaderLabels(data_table_columns)

            # fill the table starting with the row after the header

            for row in range(header_row + 1, len(self.data_lines)):
                # parse the data in memory into a list
                row_values = self.data_lines[row].strip().split(',')
                # insert a new row
                current_row = self.data_table.rowCount()
                self.data_table.insertRow(current_row)

                # Populate the row with data
                for col in range(len(data_table_columns)):
                    entry = QTableWidgetItem("{}".format(row_values[col]))
                    self.data_table.setItem(current_row, col, entry)
            print("Filled {} rows.".format(row))

        else:
            print("File not found.")

    def compute_stats(self):

        # setup an empty list to store selection data
        item_list = []
        items = self.data_table.selectedItems()
        for item in items:
            try:
                item_list.append(float(item.text()))
            except:  # some items may not be able to convert to a float.
                pass
        if len(item_list) > 1:  # Check to see if there are 2 or more samples
            # convert to an array for further analysis
            data_array = np.asarray(item_list)

            # calculate stats
            mean_value = np.mean(data_array)
            self.mean_label.setText("Mean = {:0.3f}".format(mean_value))

            # add more calculations here


# This is the main loop that starts the program. It stays at the end.
if __name__ == '__main__':
    # Start the program this way according to https://stackoverflow.com/questions/40094086/python-kernel-dies-for-second-run-of-pyqt5-gui
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    execute = StatCalculator()
    sys.exit(app.exec_())
