from PyQt6.QtWidgets import (QApplication)
import sys
from PyQt6.QtGui import QFontDatabase
import os
from View.View import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)  # deve essere prima
    font_path = os.path.join(os.path.dirname(__file__), "src", "fonts", "GothamBook.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        raise Exception("Errore nel caricamento del font Gotham")

    font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
    print(f"Font caricato: {font_family}")  # debug utile

    window = MainWindow(fontfamilyGotham=font_family)
    window.show()
    sys.exit(app.exec())