from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QDialogButtonBox

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Register')
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        register_button = QPushButton('Register')
        register_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(register_button)
        self.setLayout(layout)

    def show_register_dialog(self):
        register_dialog = RegisterDialog(self)
        if register_dialog.exec_() == QDialog.Accepted:
            # Tambahan: Mungkin tambahkan logika untuk menangani registrasi pengguna di sini
            pass
