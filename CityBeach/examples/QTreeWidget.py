from PyQt6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtGui import QBrush, QColor


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lista con Colonne (QTreeWidget)")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Nome", "Età", "Ruolo"])

        # Elemento 1
        item1 = QTreeWidgetItem(["Mario", "30", "Developer"])
        item1.setBackground(0, QBrush(QColor("lightblue")))  # Evidenzia la colonna 1
        item1.setForeground(2, QBrush(QColor("red")))  # Colore solo per il "Ruolo"
        self.tree.addTopLevelItem(item1)

        for i in range(25):
            item1 = QTreeWidgetItem(["Mario", f"{i}", "Developer"])
            self.tree.addTopLevelItem(item1)

        # Elemento 2
        item2 = QTreeWidgetItem(["Anna", "25", "Designer"])
        self.tree.addTopLevelItem(item2)

        layout.addWidget(self.tree)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec())
