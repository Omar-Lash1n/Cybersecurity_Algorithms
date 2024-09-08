from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox

class PlayfairCipherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Playfair Cipher")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Encryption/Decryption selection
        self.setGeometry(200, 200, 600, 500)

        self.operation_label = QLabel("Select Operation:")
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(["Encryption", "Decryption"])
        layout.addWidget(self.operation_label)
        layout.addWidget(self.operation_combo)

        # Plain Text / Cipher Text input
        self.text_label = QLabel("Enter Plain Text (Encryption) or Cipher Text (Decryption):")
        self.text_input = QLineEdit()
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input)

        # Key input
        self.key_label = QLabel("Enter Key:")
        self.key_input = QLineEdit()
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)

        # Result display
        self.result_label = QLabel("Result:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)

        # Process and Clear buttons
        button_layout = QHBoxLayout()
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.clear_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Apply styles
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

    def process(self):
        operation = self.operation_combo.currentText()
        text = self.text_input.text()
        key = self.key_input.text().upper()

        if not key.isalpha():
            self.result_text.setPlainText("Error: Key must contain only alphabetic characters.")
            return

        if operation == "Encryption":
            result = playfair_encrypt(text, key)
            self.result_text.setPlainText(result)
        elif operation == "Decryption":
            result = playfair_decrypt(text, key)
            self.result_text.setPlainText(result)

    def clear_fields(self):
        self.text_input.clear()
        self.key_input.clear()
        self.result_text.clear()

def generate_playfair_matrix(key):
    key = key.replace(" ", "").upper()
    key = key.replace("J", "I")
    key = "".join(dict.fromkeys(key))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    matrix = [['' for _ in range(5)] for _ in range(5)]
    key_index = 0
    alphabet_index = 0

    for i in range(5):
        for j in range(5):
            if key_index < len(key):
                matrix[i][j] = key[key_index]
                key_index += 1
            else:
                while alphabet[alphabet_index] in key:
                    alphabet_index += 1
                matrix[i][j] = alphabet[alphabet_index]
                alphabet_index += 1

    return matrix


def get_playfair_coordinates(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j


def playfair_encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "").upper()
    if not plaintext.isalpha():
        return "Error: Plain text must contain only alphabetic characters."

    plaintext = plaintext.replace("J", "I")
    plaintext_pairs = []

    # Split plaintext into pairs
    i = 0
    while i < len(plaintext):
        if i == len(plaintext) - 1 or plaintext[i] == plaintext[i + 1]:
            plaintext_pairs.append(plaintext[i] + "X")
            i += 1
        else:
            plaintext_pairs.append(plaintext[i] + plaintext[i + 1])
            i += 2

    matrix = generate_playfair_matrix(key)
    ciphertext = ""

    for pair in plaintext_pairs:
        char1, char2 = pair[0], pair[1]
        row1, col1 = get_playfair_coordinates(matrix, char1)
        row2, col2 = get_playfair_coordinates(matrix, char2)

        if row1 == row2:
            col1 = (col1 + 1) % 5
            col2 = (col2 + 1) % 5
        elif col1 == col2:
            row1 = (row1 + 1) % 5
            row2 = (row2 + 1) % 5
        else:
            col1, col2 = col2, col1

        ciphertext += matrix[row1][col1] + matrix[row2][col2]

    return ciphertext


def playfair_decrypt(ciphertext, key):
    ciphertext = ciphertext.replace(" ", "").upper()
    if not ciphertext.isalpha():
        return "Error: Cipher text must contain only alphabetic characters."

    matrix = generate_playfair_matrix(key)
    plaintext = ""

    for i in range(0, len(ciphertext), 2):
        char1, char2 = ciphertext[i], ciphertext[i + 1]
        row1, col1 = get_playfair_coordinates(matrix, char1)
        row2, col2 = get_playfair_coordinates(matrix, char2)

        if row1 == row2:
            col1 = (col1 - 1) % 5
            col2 = (col2 - 1) % 5
        elif col1 == col2:
            row1 = (row1 - 1) % 5
            row2 = (row2 - 1) % 5
        else:
            col1, col2 = col2, col1

        plaintext += matrix[row1][col1] + matrix[row2][col2]

    return plaintext

