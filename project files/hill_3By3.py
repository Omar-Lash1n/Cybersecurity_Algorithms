from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class HillCipherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hill Cipher')
        self.setGeometry(200, 200, 600, 500)

        self.word_label = QLabel('Enter a word (3, 6, or 9 letters):')
        self.word_input = QLineEdit()
        self.key_label = QLabel('Enter the key matrix (3x3):')
        self.key_input = QLineEdit()
        self.result_label = QLabel('Result:')
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)  # Set read-only property

        self.encrypt_button = QPushButton('Encrypt')
        self.decrypt_button = QPushButton('Decrypt')
        self.clear_button = QPushButton('Clear')

        # Apply styles
        self.setStyleSheet("""
            QLineEdit {
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

        # Horizontal layout for word input and key input
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.word_label)
        input_layout.addWidget(self.word_input)
        input_layout.addWidget(self.key_label)
        input_layout.addWidget(self.key_input)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.encrypt_button)
        button_layout.addWidget(self.decrypt_button)
        button_layout.addWidget(self.clear_button)

        # Vertical layout for the main window
        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)
        self.setLayout(layout)

        # Connect button signals to slots
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.clear_button.clicked.connect(self.clear)

    def encrypt(self):
        word = self.word_input.text().strip().upper()
        if len(word) not in [3, 6, 9] or not word.isalpha():
            self.show_message_box('Error', 'Please enter a valid word (3, 6, or 9 letters) containing only alphabetic characters.')
            return

        key_input = self.key_input.text().strip()
        key_matrix = self.parse_key_matrix(key_input)
        if key_matrix is None:
            self.show_message_box('Error', 'Invalid key matrix. Please try again.')
            return

        encrypted_word = hill_encrypt(word, key_matrix)
        current_text = self.result_output.toPlainText()
        self.result_output.setPlainText(current_text + f'\nEncrypted word: {encrypted_word}')

    def decrypt(self):
        word = self.word_input.text().strip().upper()
        if len(word) not in [3, 6, 9] or not word.isalpha():
            self.show_message_box('Error', 'Please enter a valid word (3, 6, or 9 letters) containing only alphabetic characters.')
            return

        key_input = self.key_input.text().strip()
        key_matrix = self.parse_key_matrix(key_input)
        if key_matrix is None:
            self.show_message_box('Error', 'Invalid key matrix. Please try again.')
            return

        decrypted_word = hill_decrypt(word, key_matrix)
        current_text = self.result_output.toPlainText()
        self.result_output.setPlainText(current_text + f'\nDecrypted word: {decrypted_word}')

    def clear(self):
        self.word_input.clear()
        self.key_input.clear()
        self.result_output.clear()

    def parse_key_matrix(self, key_input):
        try:
            elements = [int(num) for num in key_input.split()]
            if len(elements) != 9:
                return None
            key_matrix = [[elements[0], elements[1], elements[2]],
                          [elements[3], elements[4], elements[5]],
                          [elements[6], elements[7], elements[8]]]
            return key_matrix
        except ValueError:
            return None

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
