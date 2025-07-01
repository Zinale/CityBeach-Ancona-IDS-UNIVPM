from PyQt6.QtWidgets import (QApplication, QStyleFactory)
import sys
from PyQt6.QtGui import QFontDatabase
import os
from View.View import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)  # deve essere prima
    app.setStyle(QStyleFactory.create("WindowsVista"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())