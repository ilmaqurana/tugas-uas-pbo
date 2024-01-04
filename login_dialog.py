from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QDialogButtonBox


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Login')
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.check_login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        self.setLayout(layout)

    def show_login_dialog(self):
        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == QDialog.Accepted:
            self.is_authenticated = True
            self.show()

    def check_login(self):
        # You can add your logic to check the username and password here
        username = self.username_input.text()
        password = self.password_input.text()


