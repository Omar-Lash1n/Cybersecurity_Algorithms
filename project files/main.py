import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QEvent, Qt  # Import Qt from PyQt5.QtCore
from Ceaser import CaesarCipherGUI
from affine import AffineGUI
from hill_3By3 import HillCipherGUI
from hill_2By2 import HillCipher2GUI
from columnarTransposition import ColumnarTranspositionGUI
from playFair import PlayfairCipherGUI
from RSA import RSAGUI
from RailFence import RailFenceCipherGUI
from ROT13 import Rot13GUI
from SubstitutionCipher import SubstitutionCipherGUI
from Viginiere import VigenereCipherGUI

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Menu')
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("background-color: #f0f0f0;")

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        buttons = [
            ("Caesar Cipher", self.open_caesar_cipher),
            ("Affine Encryption/Decryption", self.open_affine),
            ("Hill Cipher 3x3", self.open_hill_cipher),
            ("Hill Cipher 2x2", self.open_hill_cipher2),
            ("Columnar Transposition", self.open_columnar_transposition),
            ("Playfair Cipher", self.open_playFair),
            ("RSA", self.open_RSA),
            ("Rail Fence", self.open_RailFence),
            ("Rot13", self.open_Rot13),
            ("Substitution", self.open_subistitution),
            ("Vigenere", self.open_vigenere)
        ]

        row = 0
        col = 0
        for text, callback in buttons:
            button = QPushButton(text)
            button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 24px;"
                                  "font-size: 16px; border-radius: 12px;")
            button.setFont(QFont("Arial", 12))
            button.clicked.connect(callback)
            button.setCursor(Qt.PointingHandCursor)  # Change cursor to pointing hand
            button.installEventFilter(self)  # Install event filter for hover effect
            grid_layout.addWidget(button, row, col)
            col += 1
            if col > 1:
                row += 1
                col = 0

        # Adjust the column span for the Vigenere button to center it
        vigenere_button = QPushButton("Vigenere")
        vigenere_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 24px;"
                                       "font-size: 16px; border-radius: 12px;")
        vigenere_button.setFont(QFont("Arial", 12))
        vigenere_button.clicked.connect(self.open_vigenere)
        vigenere_button.setCursor(Qt.PointingHandCursor)  # Change cursor to pointing hand
        vigenere_button.installEventFilter(self)  # Install event filter for hover effect
        grid_layout.addWidget(vigenere_button, row, 0, 1, 2)  # Vigenere button

        self.setLayout(grid_layout)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            obj.setStyleSheet("background-color: #4169E1; color: white; border: none; padding: 10px 24px;"
                              "font-size: 16px; border-radius: 12px;")
        elif event.type() == QEvent.Leave:
            obj.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 24px;"
                              "font-size: 16px; border-radius: 12px;")
        return super().eventFilter(obj, event)

    def open_caesar_cipher(self):
        self.caesar_gui = CaesarCipherGUI()
        self.caesar_gui.show()

    def open_affine(self):
        self.affine_gui = AffineGUI()
        self.affine_gui.show()

    def open_hill_cipher(self):
        self.hill_gui = HillCipherGUI()
        self.hill_gui.show()

    def open_hill_cipher2(self):
        self.hill_gui = HillCipher2GUI()
        self.hill_gui.show()

    def open_columnar_transposition(self):
        self.columnar_gui = ColumnarTranspositionGUI()
        self.columnar_gui.show()

    def open_playFair(self):
        self.playFairgui = PlayfairCipherGUI()
        self.playFairgui.show()

    def open_RSA(self):
        self.RSAgui = RSAGUI()
        self.RSAgui.show()

    def open_RailFence(self):
        self.RailFencegui = RailFenceCipherGUI()
        self.RailFencegui.show()

    def open_Rot13(self):
        self.ROT13gui = Rot13GUI()
        self.ROT13gui.show()

    def open_subistitution(self):
        self.subistitutiongui = SubstitutionCipherGUI()
        self.subistitutiongui.show()

    def open_vigenere(self):
        self.vigeneregui = VigenereCipherGUI()
        self.vigeneregui.show()

def main():
    app = QApplication(sys.argv)
    main_gui = MainGUI()
    main_gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
