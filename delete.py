import mysql.connector
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem

class DeleteWidget(QWidget):
    def __init__(self):
        super().__init__()

        # ... (previous code)

        # Connect to the MySQL database
        self.db_connection = mysql.connector.connect(
            host='lochalhost',
            user='user',
            password='',
            database='Ktm'
        )
        self.cursor = self.db_connection.cursor()

        # ... (previous code)

    def delete_data(self):
        selected_rows = self.data_table.selectionModel().selectedRows()

        # Check if any rows are selected
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Pilih baris yang akan dihapus.')
            return

        # Loop through selected rows
        for selected_row in selected_rows:
            row_index = selected_row.row()

            # Get the NPM value from the 2nd column (index 1) in the selected row
            npm = self.data_table.item(row_index, 2).text()

            # Display confirmation dialog
            confirmation = QMessageBox.question(self, 'Konfirmasi Hapus', 'Anda yakin ingin menghapus data terpilih?',
                                               QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                # Call the function to delete data based on NPM
                self.delete_contact_from_database(npm)

    def delete_contact_from_database(self, npm):
        error_message = ""  # Initialize the variable before the try block
        try:
            query = 'DELETE FROM attendance WHERE npm = %s'
            self.cursor.execute(query, (npm,))
            self.db_connection.commit()
            QMessageBox.information(self, 'Information', 'Data has been deleted.')
        except Exception as e:
            error_message = f"Failed to delete data: {str(e)}"
            QMessageBox.critical(self, 'Error', error_message)
        print(error_message)

    def closeEvent(self, event):
        # ... (previous code)
        # Call the function to create a card here
        self.create_mahasiswa_card(self.name_input.text(), self.npm_input.text(), self.program_input.text(),
                                   self.alamat_input.text(), self.tanggal_input.text())

