from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QComboBox

class CaesarCipherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caesar Cipher")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Labels and text fields
        self.setGeometry(200, 200, 600, 500)

        self.plaintext_label = QLabel("Enter Text:")
        self.plaintext_text = QLineEdit()
        self.key_label = QLabel("Enter Key:")
        self.key_text = QLineEdit()
        self.result_label = QLabel("Result:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        layout.addWidget(self.plaintext_label)
        layout.addWidget(self.plaintext_text)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_text)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        # Operation selection
        self.operation_label = QLabel("Select Operation:")
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Encrypt", "Decrypt"])
        layout.addWidget(self.operation_label)
        layout.addWidget(self.operation_combo)

        # Apply styles
        style_sheet = """
            background-color: white;
            border: 1px solid #ccc;
        """
        self.plaintext_text.setStyleSheet(style_sheet)
        self.key_text.setStyleSheet(style_sheet)
        self.result_text.setStyleSheet(style_sheet)

        self.setStyleSheet("""
                   QLabel {
                       font-weight: bold;
                   }
                   QLineEdit, QTextEdit {
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

        # Buttons layout
        button_layout = QHBoxLayout()

        # Process button
        process_button = QPushButton("Process")
        process_button.clicked.connect(self.process)
        button_layout.addWidget(process_button)

        # Clear button
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def process(self):
        plaintext = self.plaintext_text.text()
        key = self.key_text.text()
        try:
            key = int(key)
        except ValueError:
            self.result_text.setPlainText("Error: Key must be an integer.")
            return

        operation = self.operation_combo.currentText()
        if operation == "Encrypt":
            encrypted_text = self.encrypt(key, plaintext)
            self.result_text.setPlainText(encrypted_text)
        elif operation == "Decrypt":
            decrypted_text = self.decrypt(key, plaintext)
            self.result_text.setPlainText(decrypted_text)

    def encrypt(self, key, plaintext):
        encrypted_text = ''
        for char in plaintext:
            if char.isalpha():
                shift = key
                encrypted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26) + ord(
                    'a' if char.islower() else 'A'))
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt(self, key, ciphertext):
        decrypted_text = ''
        for char in ciphertext:
            if char.isalpha():
                shift = -key
                decrypted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26) + ord(
                    'a' if char.islower() else 'A'))
                decrypted_text += decrypted_char
            else:
                decrypted_text += char
        return decrypted_text

    def clear_fields(self):
        self.plaintext_text.clear()
        self.key_text.clear()
        self.result_text.clear()
