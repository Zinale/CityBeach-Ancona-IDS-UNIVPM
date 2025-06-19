from PyQt6.QtWidgets import (QApplication)
import sys

from View.View import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    #window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
