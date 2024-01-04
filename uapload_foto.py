import mysql.connector
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap

class Uapload_fotoQwidget(QWidget):
    def __init__(self):
        super().__init__()

        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='user',
            password='',
            database='Ktm'
        )
        self.cursor = self.db_connection.cursor()

        # ... (previous code)

        # Assume you have a QLabel for displaying the photo
        self.photo_label = QLabel(self)

        # Assume you have a QPushButton for triggering the upload_photo method
        upload_button = QPushButton('Upload Photo', self)
        upload_button.clicked.connect(self.upload_photo)

        # Create a QVBoxLayout to arrange widgets vertically
        layout = QVBoxLayout(self)
        layout.addWidget(self.photo_label)
        layout.addWidget(upload_button)

    def upload_photo(self):
        # Implementation of logic for selecting image file
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.png *.jpg *.bmp)")
        file_dialog.setWindowTitle("Pilih File Gambar")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            # Get the selected file path
            selected_file = file_dialog.selectedFiles()[0]

            # Display the image in QLabel
            pixmap = QPixmap(selected_file)
            self.photo_label.setPixmap(pixmap)

            # Save the file path to the database
            self.save_photo_path_to_database(selected_file)

    def save_photo_path_to_database(self, file_path):
        try:
            query = 'INSERT INTO photo_paths (path) VALUES (%s)'
            self.cursor.execute(query, (file_path,))
            self.db_connection.commit()
            print("Photo path saved to the database.")
        except Exception as e:
            error_message = f"Failed to save photo path to the database: {str(e)}"
            QMessageBox.critical(self, 'Error', error_message)
            print(error_message)

