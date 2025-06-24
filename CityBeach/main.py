from PyQt6.QtWidgets import (QApplication)
import sys
from PyQt6.QtGui import QFontDatabase
import os
from View.View import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)  # deve essere prima

    window = MainWindow()
    window.show()
    sys.exit(app.exec())