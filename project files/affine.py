from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QComboBox, QLineEdit

class AffineGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Affine Encryption/Decryption')
        self.setGeometry(200, 200, 600, 500)

        self.input_label = QLabel('Input:')
        self.output_label = QLabel('Output:')
        self.input_textedit = QTextEdit()
        self.output_textedit = QTextEdit()
        self.process_button = QPushButton('Process')
        self.process_button.clicked.connect(self.process_text)
        self.comboBox = QComboBox()
        self.comboBox.addItem("Encrypt")
        self.comboBox.addItem("Decrypt")
        self.key_a_label = QLabel('Enter key "a":')
        self.key_b_label = QLabel('Enter key "b":')
        self.key_a_edit = QLineEdit()
        self.key_b_edit = QLineEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_label)
        vbox.addWidget(self.input_textedit)
        vbox.addWidget(self.output_label)
        vbox.addWidget(self.output_textedit)
        vbox.addWidget(self.comboBox)
        vbox.addWidget(self.key_a_label)
        vbox.addWidget(self.key_a_edit)
        vbox.addWidget(self.key_b_label)
        vbox.addWidget(self.key_b_edit)
        vbox.addWidget(self.process_button)

        self.setLayout(vbox)

        # Apply styles
        style_sheet = """
            background-color: white;
            border: 1px solid #ccc;
        """
        self.input_textedit.setStyleSheet(style_sheet)
        self.output_textedit.setStyleSheet(style_sheet)
        self.key_a_edit.setStyleSheet(style_sheet)
        self.key_b_edit.setStyleSheet(style_sheet)

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

    def process_text(self):
        text = self.input_textedit.toPlainText().upper().replace(" ", "")
        try:
            if self.comboBox.currentText() == "Encrypt":
                key_a = int(self.key_a_edit.text())
                key_b = int(self.key_b_edit.text())
                key = [key_a, key_b]
                processed_text = affine_encrypt(text, key)
            else:
                key_a = int(self.key_a_edit.text())
                key_b = int(self.key_b_edit.text())
                key = [key_a, key_b]
                processed_text = affine_decrypt(text, key)
            self.output_textedit.setPlainText(processed_text)
        except ValueError:
            self.output_textedit.setPlainText("Error: Keys must be integers")
