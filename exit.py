import mysql.connector
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem

class ExitWidget(QWidget):
    def __init__(self):
        super().__init__()

        # ... (previous code)

        # Connect to the MySQL database
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='user',
            password='',
            database='Ktm'
        )
        self.cursor = self.db_connection.cursor()

        # ... (previous code)

    def closeEvent(self, event):
        # ... (previous code)

        # Call the function to create a card and save to the database
        self.create_mahasiswa_card(self.name_input.text(), self.npm_input.text(), self.program_input.text(),
                                   self.alamat_input.text(), self.tanggal_input.text())

    def create_mahasiswa_card(self, nama, npm, program, alamat, tanggal):
        # Your logic to create a card goes here
        # This is just a placeholder, replace it with your actual card creation logic
        card_info = f"Name: {nama}, NPM: {npm}, Program: {program}, Alamat: {alamat}, Tanggal: {tanggal}"
        print(f"Creating Mahasiswa Card: {card_info}")

        # Save the card information to the database
        try:
            query = '''
                INSERT INTO mahasiswa_cards (name, npm, program, alamat, tanggal)
                VALUES (%s, %s, %s, %s, %s)
            '''
            data = (nama, npm, program, alamat, tanggal)
            self.cursor.execute(query, data)
            self.db_connection.commit()
            print("Card information saved to the database.")
        except Exception as e:
            error_message = f"Failed to save card information to the database: {str(e)}"
            QMessageBox.critical(self, 'Error', error_message)
            print(error_message)
