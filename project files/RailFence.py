from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QComboBox

class RailFenceCipher:
    def __init__(self):
        pass

    def encrypt(self, plaintext, key):
        # Filter out spaces from the plaintext (spaces are ignored for encipherment)
        plaintext = "".join(plaintext.split())

        # Creation of the matrix 'rail' filled with placeholders (ph)
        rail = [['ph' for i in range(len(plaintext))] # length of plaintext = number of columns
                for j in range(key)] # key = number of rows

        # Initialized information for sense of direction and values of row/col
        direction_down = False
        col = 0
        row = 0
        for i in range(len(plaintext)):
            # Check the direction of flow (is it the first row or last row?)
            if (row == 0) or (row == key - 1):
                direction_down = not direction_down # Invert direction if yes

            # Begin filling the cipher matrix
            rail[row][col] = plaintext[i]
            col += 1

            # Change rows based on the flag variable 'direction_down' logic
            if direction_down:
                row += 1
            else:
                row -= 1

        # After the matrix has been filled, we can now extract that information to create the ciphertext
        ciphertext = []
        for i in range(key): # Rows
            for j in range(len(plaintext)): # Columns
                if rail[i][j] != 'ph': # If the value is not a placeholder, append it to the ciphertext list
                    ciphertext.append(rail[i][j])
        return "".join(ciphertext) # Convert the ciphertext list into a singular string

    def decrypt(self, ciphertext, key):
        # Creation of the matrix 'rail' filled with placeholders (similar to encryption algorithm)
        rail = [['*' for i in range(len(ciphertext))]
                for j in range(key)]

        ## Initialized information for sense of direction and values of row/col
        direction_down = None
        col = 0
        row = 0

        # Create markers on the matrix with 'mkr'
        for i in range(len(ciphertext)):
            if row == 0: # Highest level row
                direction_down = True
            if row == key - 1: # Lowest level row
                direction_down = False

            # Begin filling the matrix with markers based on the key and length of text
            rail[row][col] = 'mkr'
            col += 1

            # Change row index based on the flag variable 'direction_down' logic
            if direction_down:
                row += 1
            else:
                row -= 1

        # For loop to begin filling marked spots with characters from the ciphertext
        # idx = indexing for ciphertext, i = row index, j = col index
        idx = 0
        for i in range(key):
            for j in range(len(ciphertext)):
                if ((rail[i][j] == 'mkr') and
                        (idx < len(ciphertext))):
                    rail[i][j] = ciphertext[idx]
                    idx += 1

        # Begin reading the filled rail matrix in a zigzag manner
        plaintext = []
        col = 0
        row = 0
        for i in range(len(ciphertext)):
            if row == 0: # Highest level row
                direction_down = True
            if row == key - 1: # Lowest level row
                direction_down = False

            # Begin constructing the plaintext
            plaintext.append(rail[row][col])
            col += 1

            # Change rows based on the flag variable 'direction_down' logic
            if direction_down:
                row += 1
            else:
                row -= 1
        return "".join(plaintext) # Convert the plaintext list into a singular string


class RailFenceCipherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rail Fence Cipher")
        self.cipher = RailFenceCipher()
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
        key = self.key_text.text()
        try:
            key = int(key)
            if key < 2:
                raise ValueError("Please enter a key of 2 or more.")
        except ValueError as e:
            self.result_text.setPlainText("Error: " + str(e))
            return

        if operation == "Encrypt":
            plaintext = self.plaintext_text.text()
            encrypted_text = self.cipher.encrypt(plaintext, key)
            self.result_text.setPlainText(encrypted_text)
        elif operation == "Decrypt":
            ciphertext = self.plaintext_text.text()
            decrypted_text = self.cipher.decrypt(ciphertext, key)
            self.result_text.setPlainText(decrypted_text)

    def clear_fields(self):
        self.plaintext_text.clear()
        self.key_text.clear()
        self.result_text.clear()



