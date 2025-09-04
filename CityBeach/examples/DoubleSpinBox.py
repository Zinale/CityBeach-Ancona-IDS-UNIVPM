from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDoubleSpinBox, QLabel
import sys

class Finestra(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inserisci prezzo")

        layout = QVBoxLayout()

        self.spin = QDoubleSpinBox()
        self.spin.setPrefix("€ ")       # prefisso
        self.spin.setDecimals(2)        # due decimali
        self.spin.setRange(0.00, 9999)  # limite minimo e massimo
        self.spin.setSingleStep(0.10)   # incremento
        layout.addWidget(self.spin)

        self.label = QLabel("Prezzo selezionato: € 0.00")
        layout.addWidget(self.label)

        self.spin.valueChanged.connect(self.aggiorna_label)

        self.setLayout(layout)

    def aggiorna_label(self, valore):
        self.label.setText(f"Prezzo selezionato: € {valore:.2f}")

app = QApplication(sys.argv)
f = Finestra()
f.show()
app.exec()
