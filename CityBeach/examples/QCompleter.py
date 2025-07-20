import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QCompleter

class AutoCompleteDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Autocompletamento")
        self.setGeometry(100, 100, 300, 100)

        layout = QVBoxLayout()

        # Lista dei nomi (puoi metterci quello che vuoi)
        self.nomi = ['Alice', 'Alessandro', 'Andrea', 'Antonio', 'Anna', 'Beatrice', 'Bruno', 'Carla']

        # Campo di testo
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Inserisci un nome")

        # Completer
        self.completer = QCompleter(self.nomi, self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)  # Ignora maiuscole/minuscole
        self.input_line.setCompleter(self.completer)

        layout.addWidget(self.input_line)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoCompleteDemo()
    window.show()
    sys.exit(app.exec())
