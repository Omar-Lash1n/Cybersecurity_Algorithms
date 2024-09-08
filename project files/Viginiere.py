from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QComboBox, QColorDialog
from PyQt5.QtCore import Qt

class VigenereCipher:
    def __init__(self):
        pass

    def encrypt(self, plaintext, key):
        plaintext = plaintext.replace(" ", "")
        key_repeated = (key * (len(plaintext) // len(key))) + key[:len(plaintext) % len(key)]
        encrypted_text = ""
        for i, char in enumerate(plaintext):
            if char.isalpha():
                shift = ord(key_repeated[i].upper()) - ord('A')
                encrypted_char = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
                encrypted_text += encrypted_char if char.isupper() else encrypted_char.lower()
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt(self, ciphertext, key):
        ciphertext = ciphertext.replace(" ", "")
        key_repeated = (key * (len(ciphertext) // len(key))) + key[:len(ciphertext) % len(key)]
        decrypted_text = ""
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                shift = ord(key_repeated[i].upper()) - ord('A')
                decrypted_char = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
                decrypted_text += decrypted_char if char.isupper() else decrypted_char.lower()
            else:
                decrypted_text += char
        return decrypted_text


class VigenereCipherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vigenere Cipher")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Define colors
        self.button_color = "#4CAF50"
        self.button_hover_color = "#4169E1"
        self.button_pressed_color = "#3e8e41"
        self.label_color = "#333333"
        self.text_color = "#000000"

        self.cipher = VigenereCipher()
        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        self.setGeometry(200, 200, 600, 500)


        # Labels and text fields
        self.text_label = QLabel("Enter Text:")
        self.text_label.setStyleSheet(f"color: {self.label_color}; font-size: 14px;")
        self.text_field = QLineEdit()
        self.key_label = QLabel("Enter Key:")
        self.key_label.setStyleSheet(f"color: {self.label_color}; font-size: 14px;")
        self.key_field = QLineEdit()
        self.result_label = QLabel("Result:")
        self.result_label.setStyleSheet(f"color: {self.label_color}; font-size: 14px;")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout.addWidget(self.text_label)
        layout.addWidget(self.text_field)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_field)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        # Operation selection
        self.operation_label = QLabel("Select Operation:")
        self.operation_label.setStyleSheet(f"color: {self.label_color}; font-size: 14px;")
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Encrypt", "Decrypt"])
        layout.addWidget(self.operation_label)
        layout.addWidget(self.operation_combo)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Process button
        process_button = QPushButton("Process")
        process_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.button_color};
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.button_hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self.button_pressed_color};
            }}
        """)
        process_button.clicked.connect(self.process)
        button_layout.addWidget(process_button)

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.button_color};
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.button_hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self.button_pressed_color};
            }}
        """)
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def process(self):
        operation = self.operation_combo.currentText()
        text = self.text_field.text().upper()
        key = self.key_field.text().upper()

        if not key.isalpha():
            self.result_text.setPlainText("Error: Key must contain only alphabets.")
            return

        if operation == "Encrypt":
            encrypted_text = self.cipher.encrypt(text, key)
            self.result_text.setPlainText(encrypted_text)
        elif operation == "Decrypt":
            decrypted_text = self.cipher.decrypt(text, key)
            self.result_text.setPlainText(decrypted_text)

    def clear_fields(self):
        self.text_field.clear()
        self.key_field.clear()
        self.result_text.clear()

    def change_button_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.button_color = color.name()
            self.setStyleSheet(f"background-color: {self.button_color};")
