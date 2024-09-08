from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QMessageBox

def letter_to_number(letter):
    return ord(letter) - ord('A')

def number_to_letter(number):
    return chr(number + ord('A'))

def hill_encrypt(word, key_matrix):
    encrypted_word = ""
    for i in range(0, len(word), 2):
        vector = [letter_to_number(word[i]), letter_to_number(word[i + 1])]
        encrypted_vector = vector_matrix_multiplication(key_matrix, vector)
        encrypted_letters = [number_to_letter(num) for num in encrypted_vector]
        encrypted_word += "".join(encrypted_letters)
    return encrypted_word

def hill_decrypt(encrypted_word, key_matrix):
    decrypted_word = ""
    for i in range(0, len(encrypted_word), 2):
        vector = [letter_to_number(encrypted_word[i]), letter_to_number(encrypted_word[i + 1])]
        decrypted_vector = vector_matrix_multiplication(inverse_matrix(key_matrix), vector)
        decrypted_letters = [number_to_letter(num) for num in decrypted_vector]
        decrypted_word += "".join(decrypted_letters)
    return decrypted_word

def determinant_matrix(key_matrix):
    determinant = key_matrix[0][0] * key_matrix[1][1] - key_matrix[0][1] * key_matrix[1][0]
    return determinant

def inverse_matrix(key_matrix):
    determinant = determinant_matrix(key_matrix)
    scalar = 0
    if determinant == 0 or not len(key_matrix) == 2:
        return None
    for i in range(26):
        ecuation = (i * determinant) % 26
        if ecuation == 1:
            scalar = i
            break
    return [[(key_matrix[1][1] * scalar) % 26, ((-1 * key_matrix[0][1] % 26) * scalar) % 26],
            [((-1 * key_matrix[1][0] % 26) * scalar) % 26, (key_matrix[0][0] * scalar) % 26]]

def vector_matrix_multiplication(key_matrix, vector):
    result = [0, 0]
    for i in range(2):
        for j in range(2):
            result[i] += key_matrix[i][j] * vector[j]
            result[i] %= 26
    return result

class HillCipher2GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hill Cipher')
        self.setGeometry(200, 200, 600, 500)

        self.word_label = QLabel('Enter a word of 4 letters:')
        self.word_input = QLineEdit()
        self.key_label = QLabel('Enter the key matrix (2x2):')
        self.key_input = QLineEdit()
        self.result_label = QLabel('Result:')
        self.result_output = QTextEdit()

        self.encrypt_button = QPushButton('Encrypt')
        self.decrypt_button = QPushButton('Decrypt')
        self.clear_button = QPushButton('Clear')

        # Apply styles
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

        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.clear_button.clicked.connect(self.clear)

        layout = QVBoxLayout()
        layout.addWidget(self.word_label)
        layout.addWidget(self.word_input)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

    def encrypt(self):
        word = self.word_input.text().strip().upper()
        if len(word) != 4 or not word.isalpha():
            self.show_message_box('Error', 'Please enter a valid word of 4 letters.')
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
        if len(word) != 4 or not word.isalpha():
            self.show_message_box('Error', 'Please enter a valid word of 4 letters.')
            return

        key_input = self.key_input.text().strip()
        key_matrix = self.parse_key_matrix(key_input)
        if key_matrix is None:
            self.show_message_box('Error', 'Invalid key matrix. Please try again.')
            return

        decrypted_word = hill_decrypt(word, key_matrix)
        current_text = self.result_output.toPlainText()
        self.result_output.setPlainText(current_text + f'\nDecrypted word: {decrypted_word}')

    def parse_key_matrix(self, key_input):
        try:
            elements = [int(num) for num in key_input.split()]
            if len(elements) != 4:
                return None
            key_matrix = [[elements[0], elements[1]], [elements[2], elements[3]]]
            return key_matrix
        except ValueError:
            return None

    def clear(self):
        self.word_input.clear()
        self.key_input.clear()
        self.result_output.clear()

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()



