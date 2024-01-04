# File: ktm_app.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, \
    QTableWidgetItem, QDialog, QLabel, QFormLayout, QDialogButtonBox, QMessageBox, QFileDialog, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageDraw, ImageFont
import mysql.connector
from contact import Contact
from login_dialog import LoginDialog
from register_dialog import RegisterDialog



class KartuTandaMahasiswaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='Ktm',
        )
    
        self.cursor = self.db_connection.cursor()
        
        self.create_table_if_not_exists()
        self.is_authenticated = False
        self.login_dialog = LoginDialog(self)
        self.register_dialog = RegisterDialog(self)

        # Tambahkan widget untuk menampilkan data
        self.data_table = QTableWidget(self)
        self.data_table.setColumnCount(6)
        self.data_table.setHorizontalHeaderLabels(['ID', 'Nama', 'NPM', 'Prodi', 'Alamat', 'Tanggal'])
        self.layout.addWidget(self.data_table)

        # Tambahkan QLabel untuk menampilkan data yang disimpan
        self.saved_data_label = QLabel('Data yang disimpan:', self)
        self.layout.addWidget(self.saved_data_label)

        # Tambahkan stylesheet untuk warna latar belakang dan elemen-elemen lainnya
        self.setStyleSheet("""
            QWidget {
                background-color: lightgray;
            }
            """)

    def save_data(self):
        try:
            # Dapatkan data dari input pengguna
            name = self.name_input.text()
            npm = self.npm_input.text()
            program = self.program_input.text()
            alamat = self.alamat_input.text()
            tanggal = self.tanggal_input.text()

            # Menampilkan data yang disimpan di QLabel
            saved_data_text = f"Nama: {name}, NPM: {npm}, Prodi: {program}, Alamat: {alamat}, Tanggal: {tanggal}"
            self.saved_data_label.setText(saved_data_text)

            # Save data to the database
            contact = Contact(name, npm, program, alamat, tanggal)
            self.save_contact_to_database(contact)

            QMessageBox.information(self, 'Information', "Data sudah Disimpan!")

            # Menampilkan data ke dalam tabel setelah data disimpan
            self.show_data()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")

    def save_contact_to_database(self, contact):
        try:
            query = '''
                INSERT INTO attendance (nama, npm, prodi, alamat, tanggal)
                VALUES (?, ?, ?, ?, ?)
            '''
            self.cursor.execute(query, (contact.nama, contact.npm, contact.prodi, contact.alamat, contact.tanggal))
            self.db_connection.commit()

            self.show_data()

        except Exception:
            QMessageBox.critical(self, 'Error', f"Failed to save contact to database: {str()}")
            print(f"Failed to save contact to database: {str()}")
        
    def show_data(self):
        self.data_table.setRowCount(0)  # Menghapus data yang sudah ditampilkan sebelumnya
        try:
            query = 'SELECT * FROM attendance'
            self.cursor.execute(query)
            data = self.cursor.fetchall()

            for row_number, row_data in enumerate(data):
                self.data_table.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.data_table.setItem(row_number, column_number, item)

        except Exception as e:
            print(f"Failed to fetch data: {str(e)}")

    def create_table_if_not_exists(self):
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS attendance (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(255),
                npm VARCHAR(255),
                prodi VARCHAR(255),
                alamat VARCHAR(255),
                tanggal VARCHAR(255)
            )
            '''
            self.cursor.execute(query)
            self.db_connection.commit()
        except Exception as e:
            print(f"Error creating table: {str(e)}")


    def delete_contact_from_database(self, npm):
        try:
            query = 'DELETE FROM attendance WHERE npm = ?'
            self.cursor.execute(query, (npm,))
            self.db_connection.commit()
            QMessageBox.information(self, 'Information', 'Data telah dihapus.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to delete data: {str(e)}")
            print(f"Failed to delete data: {str(e)}")

    def init_ui(self):
        self.setGeometry(100, 100, 100, 200)
        self.setWindowTitle('Aplikasi Kartu Tanda Mahasiswa')

        self.layout = QVBoxLayout()

        self.setup_widgets()

    def setup_widgets(self):
        self.form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.npm_input = QLineEdit()
        self.program_input = QLineEdit()
        self.alamat_input = QLineEdit()
        self.tanggal_input = QLineEdit()

        self.title_label = QLabel('Kartu Tanda Mahasiswa', self)
        self.layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.form_layout.addRow('Nama:', self.name_input)
        self.form_layout.addRow('NPM:', self.npm_input)
        self.form_layout.addRow('Program Studi:', self.program_input)
        self.form_layout.addRow('Alamat:', self.alamat_input)
        self.form_layout.addRow('Tanggal Pembuatan:', self.tanggal_input)

        self.layout.addLayout(self.form_layout)

        self.photo_label = QLabel('Foto Mahasiswa')
        self.layout.addWidget(self.photo_label)

        # Tambahkan menu dropdown saat mengeklik tombol "Buat Kartu"
        self.menu_button = QPushButton('Buat Kartu', self)
        self.menu_button.clicked.connect(self.show_card_menu)
        self.layout.addWidget(self.menu_button)

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        # Tambahkan QPushButton untuk upload foto
        self.upload_button = QPushButton('Upload Foto', self)
        self.upload_button.clicked.connect(self.upload_photo)
        self.layout.addWidget(self.upload_button)

        self.delete_button = QPushButton('Hapus', self)
        self.delete_button.clicked.connect(self.delete_data)
        self.layout.addWidget(self.delete_button)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.close)
        self.layout.addWidget(self.exit_button)

        self.informasi_label = QLabel('Klik Buat Kartu jika data yang dimasukkan sudah benar.', self)
        self.layout.addWidget(self.informasi_label)

        self.setLayout(self.layout)

    def save_data(self):
        e = None  # Initialize the variable before the try block
        try:
        # Dapatkan data dari input pengguna
            name = self.name_input.text()
            npm = self.npm_input.text()
            program = self.program_input.text()
            alamat = self.alamat_input.text()
            tanggal = self.tanggal_input.text()

        # Menampilkan data yang disimpan di QLabel
            saved_data_text = f"Nama: {name}, NPM: {npm}, Prodi: {program}, Alamat: {alamat}, Tanggal: {tanggal}"
            self.saved_data_label.setText(saved_data_text)

        # Save data to the database
            contact = Contact(name, npm, program, alamat, tanggal)
            self.save_contact_to_database(contact)

            QMessageBox.information(self, 'Information', "Data sudah Disimpan!")

        # Menampilkan data ke dalam tabel setelah data disimpan
            self.show_data()
        except Exception as ex:
            e = ex  # Update the variable if an exception occurs
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")
        print(e)  # This will print the exception message or None if no exception occurred


    def save_contact_to_database(self, contact):
        try:
            query = '''
            INSERT INTO attendance (nama, npm, prodi, alamat, tanggal)
            VALUES (%s, %s, %s, %s, %s)
        '''
            self.cursor.execute(query, (contact.nama, contact.npm, contact.prodi, contact.alamat, contact.tanggal))
            self.db_connection.commit()

            self.show_data()

        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to save contact to database: {str(e)}")
        print(f"Failed to save contact to database: {str(e)}")

    def show_card_menu(self):
        menu = QMenu(self)

        # Tambahkan opsi menu
        manual_action = QAction('Buat Kartu Manual', self)
        manual_action.triggered.connect(self.generate_card_manual)
        menu.addAction(manual_action)

        automatic_action = QAction('Buat Kartu Otomatis', self)
        automatic_action.triggered.connect(self.generate_card_automatic)
        menu.addAction(automatic_action)

        # Tampilkan menu di posisi tombol
        menu.exec_(self.menu_button.mapToGlobal(self.menu_button.pos()))

    def generate_card_manual(self):
        # Dapatkan data dari input pengguna atau dari data yang sudah ada
        name = self.name_input.text()
        npm = self.npm_input.text()
        program = self.program_input.text()
        alamat = self.alamat_input.text()
        tanggal = self.tanggal_input.text()

        # Implementasikan logika pembuatan kartu manual di sini

        # Implementasi logika pemilihan file gambar
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.png *.jpg *.bmp)")
        file_dialog.setWindowTitle("Pilih File Gambar")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            # Dapatkan path file yang dipilih
            selected_file = file_dialog.selectedFiles()[0]

            # Set teks pada label foto
            self.photo_label.setText(f"Nama: {name}\nNPM: {npm}\nProgram Studi: {program}\nAlamat: {alamat}\nTanggal Pembuatan: {tanggal}")

            # Misalnya, menggunakan QLabel untuk menampilkan informasi kartu
            card_text = f"Nama: {name}\nNPM: {npm}\nProgram Studi: {program}\nAlamat: {alamat}\nTanggal Pembuatan: {tanggal}"

            # Set teks pada label foto
            self.photo_label.setText(card_text)

            # Jika Anda ingin menyimpan gambar kartu, implementasikan logika penyimpanan di sini
            # Misalnya, menggunakan library seperti Pillow untuk membuat gambar dan menyimpannya
            # Simpan kartu sebagai gambar
            self.save_card_to_image(selected_file, card_text)

    def save_card_to_image(self, file_path, card_text):
        try:
            # Contoh penyimpanan gambar menggunakan Pillow
            image = Image.new('RGB', (50, 50), color='white')
            draw = ImageDraw.Draw(image)
            font = ImageFont.load_default()

            # Atur teks pada gambar
            draw.text((10, 10), card_text, fill='black', font=font)

            # Simpan gambar sebagai file
            image.save(file_path)
            QMessageBox.information(self, 'Information', f"Kartu disimpan sebagai {file_path}")
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to save card to image: {str(e)}")

    def generate_card_automatic(self):
        # Dapatkan data dari database atau sumber data lainnya
        # Implementasikan logika pembuatan kartu otomatis di sini
        # Misalnya, menggunakan QLabel untuk menampilkan informasi kartu
        card_text = "Informasi Kartu Otomatis"

        # Set teks pada label foto
        self.photo_label.setText(card_text)

        # Jika Anda ingin menyimpan gambar kartu, implementasikan logika penyimpanan di sini
        # Misalnya, menggunakan library seperti Pillow untuk membuat gambar dan menyimpannya

        # Contoh penyimpanan gambar menggunakan Pillow
        # from PIL import Image, ImageDraw, ImageFont
        # image = Image.new('RGB', (width, height), color='white')
        # draw = ImageDraw.Draw(image)
        # font = ImageFont.load_default()
        # draw.text((x, y), card_text, fill='black', font=font)
        # image.save('kartu_mahasiswa.png')

    def create_new_data(self):
        # Your implementation for creating new data
        QMessageBox.information(self, 'Information', "Create New Data")
        print("Create New Data")

    def upload_photo(self):
        # Implementasi logika pemilihan file gambar
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.png *.jpg *.bmp)")
        file_dialog.setWindowTitle("Pilih File Gambar")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec_():
            # Dapatkan path file yang dipilih
            selected_file = file_dialog.selectedFiles()[0]

            # Tampilkan gambar di QLabel
            pixmap = QPixmap(selected_file)
            self.photo_label.setPixmap(pixmap)

    def delete_data(self):
        selected_rows = self.data_table.selectionModel().selectedRows()

        # Periksa apakah ada baris yang dipilih
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Pilih baris yang akan dihapus.')
            return

        # Loop melalui baris yang dipilih
        for selected_row in selected_rows:
            row_index = selected_row.row()

            # Dapatkan nilai NPM dari kolom ke-2 (indeks 1) dalam baris yang dipilih
            npm = self.data_table.item(row_index, 2).text()

            # Tampilkan dialog konfirmasi
            confirmation = QMessageBox.question(self, 'Konfirmasi Hapus', 'Anda yakin ingin menghapus data terpilih?',
            QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                # Panggil fungsi untuk menghapus data berdasarkan NPM
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
    # Panggil fungsi untuk membuat kartu di sini
        self.create_mahasiswa_card(self.name_input.text(), self.npm_input.text(), self.program_input.text(), self.alamat_input.text(), 
                                   self.tanggal_input.text())


    def create_mahasiswa_card(self, name, npm, program, alamat, tanggal):
        # Implementasikan logika pembuatan kartu di sini
        # Misalnya, Anda dapat menggunakan library seperti Pillow untuk manipulasi gambar
        # dan menyimpannya sebagai file gambar kartu

        # Contoh sederhana
        card_text = f"Nama: {name}\nNPM: {npm}\nProgram Studi: {program}\nAlamat: {alamat}\nTanggal Pembuatan: {tanggal}"
        self.photo_label.setText(card_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = KartuTandaMahasiswaApp()
    main_app.show()
    sys.exit(app.exec_())
    