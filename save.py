import mysql.connector
from contact import Contact
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox

class SaveDataWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Assume you have QLineEdit widgets for user input and a QLabel for displaying saved data
        self.nama_input = QLineEdit(self)
        self.npm_input = QLineEdit(self)
        self.program_input = QLineEdit(self)
        self.alamat_input = QLineEdit(self)
        self.tanggal_input = QLineEdit(self)
        self.saved_data_label = QLabel(self)

        # Connect to the MySQL database
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='user',
            password='password',
            database='Ktm'
        )
        self.cursor = self.db_connection.cursor()

        # Assume you have a QPushButton for triggering the save_data method
        save_button = QPushButton('Save Data', self)
        save_button.clicked.connect(self.save_data)

        # You may also have a method for initializing the UI
        self.init_ui()

    def init_ui(self):
        # Arrange your widgets here as needed
        pass

    def save_data(self):
        try:
            # Get data from user input
            nama = self.nama_input.text()
            npm = self.npm_input.text()
            program = self.program_input.text()
            alamat = self.alamat_input.text()
            tanggal = self.tanggal_input.text()

            # Display saved data in QLabel
            saved_data_text = f"Nama: {nama}, NPM: {npm}, Prodi: {program}, Alamat: {alamat}, Tanggal: {tanggal}"
            self.saved_data_label.setText(saved_data_text)

            # Save data to the MySQL database
            contact = Contact(nama, npm, program, alamat, tanggal)
            self.save_contact_to_database(contact)

            QMessageBox.information(self, 'Information', "Data sudah Disimpan!")

            # Display data in the table after saving data
            self.show_data()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")

    def save_contact_to_database(self, contact):
        try:
            query = '''
                INSERT INTO attendance (nama, npm, prodi, alamat, tanggal)
                VALUES (%s, %s, %s, %s, %s)
            '''
            data = (contact.nama, contact.npm, contact.prodi, contact.alamat, contact.tanggal)
            self.cursor.execute(query, data)
            self.db_connection.commit()

            self.show_data()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred while saving to the database: {str(e)}")
            print(f"An error occurred while saving to the database: {str(e)}")

    def show_data(self):
        # Implement the method to display data in your table or update the UI as needed
        pass

