from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QSplitter
)
from PyQt6.QtCore import Qt
import sys

app = QApplication(sys.argv)

# Finestra principale
main_window = QWidget()
main_layout = QVBoxLayout(main_window)

# Splitter orizzontale
splitter = QSplitter(Qt.Orientation.Horizontal)

# Primo widget (metà finestra) con QHBoxLayout
left_widget = QWidget()
left_layout = QHBoxLayout(left_widget)
left_layout.addWidget(QPushButton("Bottone 1"))
left_layout.addWidget(QPushButton("Bottone 2"))

# Secondo widget (l'altra metà)
right_widget = QWidget()

# Aggiungi widget allo splitter
splitter.addWidget(left_widget)
splitter.addWidget(right_widget)

# Imposta le proporzioni (metà e metà)
splitter.setSizes([1, 1])  # Puoi anche usare [300, 300] se vuoi dimensioni iniziali precise

# Aggiungi lo splitter al layout principale
main_layout.addWidget(splitter)

main_window.resize(600, 400)
main_window.show()
sys.exit(app.exec())
