# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, QLabel, QTableWidget, \
    QTableWidgetItem, QTextEdit
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from Service import userFunc, sourceFunc, exportFunc, emailFunc, complaintFunc
from model import user, source


class Dashboard(QWidget):
    def __init__(self):
        super(Dashboard, self).__init__()

        # initialize nodes from add users tab
        self.user_table = None
        self.addUser_warning_label = None
        self.addUser_success_label = None
        self.addUser_authority_selector = None
        self.addUser_password_input = None
        self.addUser_email_input = None
        self.addUser_username_input = None
        self.addUser_name_input = None
        self.addUser_btn = None

        # Initialize nodes from add source
        self.moderator_selector = None
        self.sourceName_input = None
        self.sourceLocation_input = None
        self.sourceType_selector = None
        self.sourceStatus_input = None
        self.sourceCapacity_input = None
        self.waterLevel_input = None
        self.addSource_success_message = None
        self.addSource_error_message = None
        self.addSource_btn = None

        # Initialize dashboard nodes
        self.source_table = None
        self.export_data_btn = None
        self.email_btn = None
        self.complaint_details = None

        # initialize complaint nodes
        self.source_selector = None
        self.complaint_success_message = None
        self.complaint_error_message = None
        self.submit_complaint_btn = None
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "main-view.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

        # Fill the user_table with all available users' info
        users = userFunc.get_all_users()  # Retrieve the list of users from the database

        self.source_table = self.findChild(QTableWidget, "source_table")
        sources = sourceFunc.get_all_sources()
        self.populate_source_table(sources)

        # Fill the source_selector with all available users' info
        self.source_selector = self.findChild(QComboBox, "source_selector")
        sources = sourceFunc.get_all_sources()  # Retrieve the list of users from the database
        self.populate_source_selector(sources)  # Populate the user_table with the retrieved users

        # get nodes from add users tab
        self.addUser_btn = self.findChild(QPushButton, "addUser_btn")
        self.addUser_btn.clicked.connect(self.add_user_clicked)  # call function to add user on click of button
        self.addUser_name_input = self.findChild(QLineEdit, "addUser_name_input")
        self.addUser_username_input = self.findChild(QLineEdit, "addUser_username_input")
        self.addUser_email_input = self.findChild(QLineEdit, "addUser_email_input")
        self.addUser_password_input = self.findChild(QLineEdit, "addUser_password_input")
        self.addUser_authority_selector = self.findChild(QComboBox, "addUser_authority_selector")
        self.addUser_success_label = self.findChild(QLabel, "addUser_success_label")
        self.addUser_warning_label = self.findChild(QLabel, "addUser_warning_label")

        # get nodes from add source tab
        self.sourceName_input = self.findChild(QLineEdit, "sourceName_input")
        self.sourceLocation_input = self.findChild(QLineEdit, "sourceLocation_input")
        self.sourceType_selector = self.findChild(QComboBox, "sourceType_selector")
        self.sourceStatus_input = self.findChild(QComboBox, "sourceStatus_input")
        self.sourceCapacity_input = self.findChild(QLineEdit, "sourceCapacity_input")
        self.waterLevel_input = self.findChild(QLineEdit, "waterLevel_input")
        self.addSource_success_message = self.findChild(QLabel, "addSource_success_message")
        self.addSource_error_message = self.findChild(QLabel, "addSource_error_message")
        self.addSource_btn = self.findChild(QPushButton, "addSource_btn")
        self.addSource_btn.clicked.connect(self.add_source_clicked)  # Call function to add source on button clicked

        self.export_data_btn = self.findChild(QPushButton, "export_data")
        self.export_data_btn.clicked.connect(self.export_to_spreadsheet)

        self.email_btn = self.findChild(QPushButton, "email_btn")
        self.email_btn.clicked.connect(self.send_email)

        self.complaint_details = self.findChild(QTextEdit, "complaint_details")
        self.complaint_success_message = self.findChild(QLabel, "complaint_success_message")
        self.complaint_error_message = self.findChild(QLabel, "complaint_error_message")
        self.submit_complaint_btn = self.findChild(QPushButton, "submit_complaint_btn")
        self.submit_complaint_btn.clicked.connect(self.submit_complaint)

    def populate_source_table(self, sources):
        self.source_table.setRowCount(len(sources))
        for row, table_source in enumerate(sources):
            name_item = QTableWidgetItem(table_source.name)
            location_item = QTableWidgetItem(table_source.location)
            type_item = QTableWidgetItem(table_source.type)
            capacity_item = QTableWidgetItem(str(table_source.capacity))
            status_item = QTableWidgetItem(table_source.status)
            water_leve_item = QTableWidgetItem(str(table_source.water_level))
            approvers_item = QTableWidgetItem(table_source.approvers)
            self.source_table.setItem(row, 0, name_item)
            self.source_table.setItem(row, 1, location_item)
            self.source_table.setItem(row, 2, type_item)
            self.source_table.setItem(row, 3, capacity_item)
            self.source_table.setItem(row, 4, status_item)
            self.source_table.setItem(row, 5, water_leve_item)
            self.source_table.setItem(row, 6, approvers_item)

    def add_user_clicked(self):
        name = self.addUser_name_input.text()
        username = self.addUser_username_input.text()
        email = self.addUser_email_input.text()
        password = self.addUser_password_input.text()
        authority = self.addUser_authority_selector.currentText()

        result = userFunc.add_user(name, username, email, password, authority)
        if isinstance(result, user.User):
            self.addUser_success_label.setText("User was added successfully!")
            self.clear_add_user_fields()
        else:
            self.addUser_warning_label.setText(result)

    def add_source_clicked(self):
        s_name = self.sourceName_input.text()
        s_location = self.sourceLocation_input.text()
        s_type = self.sourceType_selector.currentText()
        s_capacity = self.sourceCapacity_input.text()
        s_status = self.sourceStatus_input.currentText()
        s_water_level = self.waterLevel_input.text()
        result = sourceFunc.add_source(s_name, s_location, s_type, s_capacity, s_status, s_water_level)

        if isinstance(result, source.Source):
            self.add_source_to_table(s_name, s_location, s_type, s_capacity, s_status, s_water_level)
            self.addSource_success_message.setText("source added successfully")
            self.clear_add_source_fields()
        else:
            self.addSource_error_message.setText(result)
        # check if a source object is being returned if so, i will hanlde it, else disaplay the warning messaged in
        # self.addSource_error_message

    def clear_add_user_fields(self):
        self.addUser_name_input.clear()
        self.addUser_username_input.clear()
        self.addUser_email_input.clear()
        self.addUser_password_input.clear()
        self.addUser_authority_selector.setCurrentIndex(0)

    def add_source_to_table(self, name, location, s_type, capacity, status, water_level):
        row = self.source_table.rowCount()
        self.source_table.insertRow(row)

        name_item = QTableWidgetItem(name)
        location_item = QTableWidgetItem(location)
        type_item = QTableWidgetItem(s_type)
        capacity_item = QTableWidgetItem(capacity)
        status_item = QTableWidgetItem(status)
        water_leve_item = QTableWidgetItem(water_level)

        self.source_table.setItem(row, 0, name_item)
        self.source_table.setItem(row, 1, location_item)
        self.source_table.setItem(row, 2, type_item)
        self.source_table.setItem(row, 3, capacity_item)
        self.source_table.setItem(row, 4, status_item)
        self.source_table.setItem(row, 5, water_leve_item)

    def populate_source_selector(self, sources):
        for water_source in sources:
            # Assuming the 'type' attribute of the Authority object is the one to be displayed
            source_name = water_source.name
            self.add_items_to_source_selectors(source_name)

    def export_to_spreadsheet(self):
        # Get selected row from self.source_table (using QTableWidget) and its column data
        selected_row = self.source_table.currentRow()
        column_data = []
        for column in range(self.source_table.columnCount()):
            item = self.source_table.item(selected_row, column)
            column_data.append(item.text())

        # Call a function that takes the column data as arguments
        exportFunc.export_data_to_spreadsheet(*column_data)

    def send_email(self):
        selected_row = self.source_table.currentRow()
        source_name = self.source_table.item(selected_row, 0).text()

        # Get the source with the name equal to the column data
        email_source = sourceFunc.get_source_by_name(source_name)

        # Prepare email content
        subject = "[Warning message for water source]"
        body = f"Source Information:\n\n" \
               f"Name: {email_source.name}\n" \
               f"Location: {email_source.location}\n" \
               f"Type: {email_source.type}\n" \
               f"Capacity: {email_source.capacity}\n" \
               f"Status: {email_source.status}\n" \
               f"Water Level: {email_source.water_level}\n" \
               f"Approvers: {email_source.approvers}\n"

        # Send email
        emailFunc.send_email_to_recipient("alimohamedamir124@gmail.com", subject, body)

    def clear_add_source_fields(self):
        self.sourceName_input.setText("")
        self.sourceLocation_input.setText("")
        self.sourceCapacity_input.setText("")
        self.waterLevel_input.setText("")

    def add_items_to_moderator_selectors(self, item):
        self.moderator_selector.addItem(item)

    def add_items_to_source_selectors(self, item):
        self.source_selector.addItem(item)

    def submit_complaint(self):
        result = complaintFunc.submit_complaint(self.source_selector.currentText(),
                                                self.complaint_details.toPlainText())
        if result == "success":
            self.complaint_success_message.setText("Complaint submitted successfully")
            self.complaint_details.setText("")
        else:
            self.complaint_error_message.setText(result)


if __name__ == "__main__":
    app = QApplication([])
    widget = Dashboard()
    widget.show()
    sys.exit(app.exec())
