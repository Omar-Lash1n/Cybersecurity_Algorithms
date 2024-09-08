import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from random import shuffle


def gcd(a, b):
    """Calculates the greatest common divisor (GCD) of two integers."""
    while b != 0:
        a, b = b, a % b
    return a


def is_prime(n):
    """Checks if a number is prime."""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def generate_keys(p, q):
    """Generates a public key (e, n) and a private key (d, n) based on the given primes p and q."""
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 2  # Public exponent
    while e < phi:
        if gcd(e, phi) == 1:
            break
        else:
            e += 1

    k = 2  # Private exponent multiplier
    d = (1 + (k * phi)) // e  # Integer division for d

    return ((e, n), (d, n), n)  # Public key, private key, and modulus n tuples


def encrypt_message(message, public_key):
    """Encrypts the given message character-by-character using the provided public key (e, n)."""
    e, n = public_key
    encrypted_message = []
    for char in message:
        msg_int = ord(char)  # Convert each character to integer
        c = pow(msg_int, e, n)  # Encrypted integer code
        encrypted_message.append(c)  # Add to encrypted message list
    return encrypted_message  # Return list of encrypted integer codes


def decrypt_message(encrypted_message, private_key):
    """Decrypts the given encrypted message using the provided private key (d, n)."""
    d, n = private_key
    decrypted_message = ""
    for c in encrypted_message:
        m = pow(c, d, n)  # Decrypted integer code
        decrypted_char = chr(m)  # Convert integer back to character
        decrypted_message += decrypted_char  # Append to decrypted message string
    return decrypted_message


class RSAGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RSA Encryption/Decryption')
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
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_text)
        self.mode_label = QLabel('Mode:')
        self.mode_combobox = QComboBox()
        self.mode_combobox.addItem("Encrypt")
        self.mode_combobox.addItem("Decrypt")

        self.prime_pairs_label = QLabel('Prime Number Pairs:')
        self.prime_pairs_combobox = QComboBox()
        self.prime_pairs = [
            (7, 23),
            (11, 29),
            (29, 47),
            (47, 71),
            (13, 31),
            (43, 67),
            (11, 47),
            (11, 71),
            (7, 43),
            (29, 47)
        ]
        for pair in self.prime_pairs:
            self.prime_pairs_combobox.addItem(f"{pair[0]}-{pair[1]}")

        self.key_c_label = QLabel('Modulus n:')
        self.key_d_label = QLabel('Private key (d):')
        self.key_c_edit = QLineEdit()
        self.key_d_edit = QLineEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.input_textedit)
        vbox.addWidget(self.output_label)
        vbox.addWidget(self.output_textedit)
        hbox_mode = QHBoxLayout()
        hbox_mode.addWidget(self.mode_label)
        hbox_mode.addWidget(self.mode_combobox)
        vbox.addLayout(hbox_mode)
        hbox_pairs = QHBoxLayout()
        hbox_pairs.addWidget(self.prime_pairs_label)
        hbox_pairs.addWidget(self.prime_pairs_combobox)
        vbox.addLayout(hbox_pairs)
        vbox.addWidget(self.key_c_label)
        vbox.addWidget(self.key_c_edit)
        vbox.addWidget(self.key_d_label)
        vbox.addWidget(self.key_d_edit)

        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.process_button)
        hbox_buttons.addWidget(self.clear_button)
        vbox.addLayout(hbox_buttons)

        self.setLayout(vbox)

    def process_text(self):
        text = self.input_textedit.toPlainText()
        mode = self.mode_combobox.currentText()
        if mode == "Encrypt":
            index = self.prime_pairs_combobox.currentIndex()
            p, q = self.prime_pairs[index]
            public_key, private_key, modulus = generate_keys(p, q)
            if public_key is None:
                self.output_textedit.setPlainText("Error: Unable to generate keys with given p and q")
                return
            encrypted_message = encrypt_message(text, public_key)
            self.output_textedit.setPlainText("Encrypted message: {}".format(encrypted_message))
            self.key_c_edit.setText(str(modulus))
            self.key_d_edit.setText(str(private_key[0]))
        elif mode == "Decrypt":
            if not text:
                self.output_textedit.setPlainText("Error: No input provided for decryption")
                return
            if not all(char.isdigit() or char == ',' or char.isspace() for char in text):
                self.output_textedit.setPlainText("Error: Input contains non-numeric characters")
                return
            try:
                n = int(self.key_c_edit.text())
                d = int(self.key_d_edit.text())
                encrypted_message = [int(x) for x in text.split(',')]
                decrypted_message = decrypt_message(encrypted_message, (d, n))
                self.output_textedit.setPlainText("Decrypted message: {}".format(decrypted_message))
            except ValueError:
                self.output_textedit.setPlainText("Error: Modulus n and private key d must be integers")
                return

    def clear_text(self):
        self.input_textedit.clear()
        self.output_textedit.clear()
        self.key_c_edit.clear()
        self.key_d_edit.clear()

