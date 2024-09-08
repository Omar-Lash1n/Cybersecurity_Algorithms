from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtGui import QColor

class SubstitutionCipherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Substitution Cipher Encryption/Decryption Tool")
        self.init_ui()

    def init_ui(self):
        # Set background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(230, 230, 250))
        self.setPalette(p)
        self.setGeometry(200, 200, 600, 500)


        self.text_edit = QTextEdit()
        self.key_edit = QLineEdit()
        self.output_edit = QTextEdit()

        # Set styles for widgets
        self.setStyleSheet(
            """
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
            """
        )

        self.encryption_button = QPushButton("Encryption")
        self.decryption_button = QPushButton("Decryption")
        self.clear_button = QPushButton("Clear")

        self.encryption_button.clicked.connect(self.encrypt_message)
        self.decryption_button.clicked.connect(self.decrypt_message)
        self.clear_button.clicked.connect(self.clear_fields)

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Enter Text:"))
        input_layout.addWidget(self.text_edit)
        input_layout.addWidget(QLabel("Enter Key:"))
        input_layout.addWidget(self.key_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.encryption_button)
        button_layout.addWidget(self.decryption_button)
        button_layout.addWidget(self.clear_button)

        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("Output:"))
        output_layout.addWidget(self.output_edit)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

    def encrypt_message(self):
        plaintext = self.text_edit.toPlainText()
        key = self.key_edit.text()

        try:
            result = substitution_cipher(plaintext, key, "encryption")
            self.output_edit.setText(result)
        except ValueError as e:
            self.output_edit.setText(str(e))

    def decrypt_message(self):
        plaintext = self.text_edit.toPlainText()
        key = self.key_edit.text()

        try:
            result = substitution_cipher(plaintext, key, "decryption")
            self.output_edit.setText(result)
        except ValueError as e:
            self.output_edit.setText(str(e))

    def clear_fields(self):
        self.text_edit.clear()
        self.key_edit.clear()
        self.output_edit.clear()

def substitution_cipher(plaintext, key, mode):
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    if len(key) != len(alphabet):
        raise ValueError("Key length must be equal to the alphabet length (26).")

    if len(set(key.lower())) != len(alphabet):
        raise ValueError("Key must contain 26 unique characters.")

    if mode not in ("encryption", "decryption"):
        raise ValueError("Invalid mode. Please choose 'encryption' or 'decryption'.")

    ciphertext = ""
    if mode == "encryption":
        for char in plaintext:
            if char.lower() in alphabet:
                index = alphabet.index(char.lower())
                ciphertext += key[index] if char.isupper() else key[index].lower()
            else:
                ciphertext += char
    elif mode == "decryption":
        inverse_key_dict = {char.lower(): key.index(char.lower()) for char in key}
        for char in plaintext:
            if char.lower() in inverse_key_dict:
                index = inverse_key_dict[char.lower()]
                ciphertext += alphabet[index] if char.isupper() else alphabet[index].lower()
            else:
                ciphertext += char
    return ciphertext
