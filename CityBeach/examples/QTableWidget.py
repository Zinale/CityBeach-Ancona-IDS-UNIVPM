from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout
from PyQt6.QtGui import QBrush, QColor

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabella con PyQt6")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.table = QTableWidget(3, 3)  # 3 righe, 3 colonne
        self.table.setHorizontalHeaderLabels(["Nome", "Età", "Ruolo"])

        # Riga 0
        self.table.setItem(0, 0, QTableWidgetItem("Luca"))
        item_role = QTableWidgetItem("Manager")
        item_role.setForeground(QBrush(QColor("green")))
        self.table.setItem(0, 2, item_role)

        # Riga 1 con evidenziazione completa
        for col, text in enumerate(["Sara", "28", "Analyst"]):
            item = QTableWidgetItem(text)
            item.setBackground(QBrush(QColor("lightyellow")))
            self.table.setItem(1, col, item)

        layout.addWidget(self.table)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
