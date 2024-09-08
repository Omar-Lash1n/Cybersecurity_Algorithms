from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox
from PyQt5.QtGui import QFont


class Rot13GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.rot13 = Rot13()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ROT13 Encryption/Decryption')
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("""
            QTextEdit, QLineEdit {
                background-color: white;
                border: 1px solid black;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4169E1;
            }
            """)

        self.input_label = QLabel('Input:')
        self.output_label = QLabel('Output:')
        self.input_textedit = QTextEdit()
        self.output_textedit = QTextEdit()
        self.process_button = QPushButton('Process')
        self.process_button.clicked.connect(self.process_text)
        self.comboBox = QComboBox()
        self.comboBox.addItem("Encrypt")
        self.comboBox.addItem("Decrypt")

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.input_textedit)
        vbox.addWidget(self.output_label)
        vbox.addWidget(self.output_textedit)
        vbox.addWidget(self.comboBox)
        vbox.addWidget(self.process_button)

        self.setLayout(vbox)

    def process_text(self):
        text = self.input_textedit.toPlainText()
        if self.comboBox.currentText() == "Encrypt":
            processed_text = self.rot13.encrypt(text)
        else:
            processed_text = self.rot13.decrypt(text)
        self.output_textedit.setPlainText(processed_text)


class Rot13:
    def __init__(self):
        pass

    def encrypt(self, plaintext):
        encrypted_text = ''
        for char in plaintext:
            if char.isalpha():
                shift = 13 if char.islower() else -13
                encrypted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26) + ord(
                    'a' if char.islower() else 'A'))
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt(self, ciphertext):
        decrypted_text = ''
        for char in ciphertext:
            if char.isalpha():
                shift = -13 if char.islower() else 13
                decrypted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26) + ord(
                    'a' if char.islower() else 'A'))
                decrypted_text += decrypted_char
            else:
                decrypted_text += char
        return decrypted_text


