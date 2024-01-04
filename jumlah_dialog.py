from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QDialogButtonBox

class JumlahDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QFormLayout()

        self.label_jumlah = QLabel("Jumlah:")
        self.input_jumlah = QLineEdit(self)
        self.layout.addRow(self.label_jumlah, self.input_jumlah)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)