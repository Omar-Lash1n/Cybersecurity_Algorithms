from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
import math

class ColumnarTranspositionGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Columnar Transposition")
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            ColumnarTranspositionGUI {
                background-color: #f0f0f0;
            }
            QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #4169E1;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        self.setGeometry(200, 200, 600, 500)

        self.text_edit = QLineEdit()
        self.key_edit = QLineEdit()
        self.result_edit = QTextEdit()
        self.result_edit.setReadOnly(True)

        self.encryption_button = QPushButton("Encryption")
        self.decryption_button = QPushButton("Decryption")
        self.clear_button = QPushButton("Clear")

        self.encryption_button.clicked.connect(self.encrypt_message)
        self.decryption_button.clicked.connect(self.decrypt_message)
        self.clear_button.clicked.connect(self.clear_fields)

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Enter Text:"))
        input_layout.addWidget(self.text_edit)
        input_layout.addWidget(QLabel("Enter Key (Letters and Integers only):"))
        input_layout.addWidget(self.key_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.encryption_button)
        button_layout.addWidget(self.decryption_button)
        button_layout.addWidget(self.clear_button)

        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("Result:"))
        output_layout.addWidget(self.result_edit)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(output_layout)

        self.setLayout(main_layout)

    def encrypt_message(self):
        plaintext = self.text_edit.text().replace(" ", "")
        key = self.key_edit.text()

        if not key.isalnum():
            self.result_edit.setText("Invalid key input. Key must contain only letters and integers.")
            return

        cipher = self.encrypt_message_logic(plaintext, key)
        self.result_edit.setText(cipher)

    def decrypt_message(self):
        ciphertext = self.text_edit.text()
        key = self.key_edit.text()

        if not key.isalnum():
            self.result_edit.setText("Invalid key input. Key must contain only letters and integers.")
            return

        decrypted_message = self.decrypt_message_logic(ciphertext, key)
        self.result_edit.setText(decrypted_message)

    def clear_fields(self):
        self.text_edit.clear()
        self.key_edit.clear()
        self.result_edit.clear()

    def encrypt_message_logic(self, msg, key):
        cipher = ""
        k_indx = 0
        msg_len = float(len(msg))
        msg_lst = list(msg)
        key_lst = sorted(list(key))
        col = len(key)
        row = int(math.ceil(msg_len / col))
        fill_null = int((row * col) - msg_len)
        msg_lst.extend(' ' * fill_null)  # Padding with spaces
        matrix = [msg_lst[i: i + col] for i in range(0, len(msg_lst), col)]

        for _ in range(col):
            curr_idx = key.index(key_lst[k_indx])
            cipher += ''.join([row[curr_idx] for row in matrix])
            k_indx += 1

        return cipher

    def decrypt_message_logic(self, cipher, key):
        msg = ""
        k_indx = 0
        msg_len = len(cipher)
        col = len(key)
        row = int(math.ceil(msg_len / col))
        key_lst = sorted(list(key))
        dec_cipher = []

        # Create a matrix with appropriate dimensions
        for _ in range(row):
            dec_cipher.append([''] * col)

        # Arrange the matrix column wise according to permutation order by adding into new matrix
        for _ in range(col):
            curr_idx = key.index(key_lst[k_indx])

            for j in range(row):
                if k_indx * row + j < msg_len:
                    dec_cipher[j][curr_idx] = cipher[k_indx * row + j]
            k_indx += 1

        # Extract the message from the matrix
        for i in range(row):
            for j in range(col):
                msg += dec_cipher[i][j]

        return msg.rstrip()  # Remove trailing spaces


