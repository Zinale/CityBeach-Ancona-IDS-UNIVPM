import sys

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import *

class add_Dipendete_ui(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Dipendente")
        self.setFixedSize(300, 280)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.nome = QLineEdit()
        self.cognome = QLineEdit()
        self.username = QLineEdit()

        self.data_nascita = QDateEdit()
        self.data_nascita.setDisplayFormat("dd/MM/yyyy")
        self.data_nascita.setCalendarPopup(True)
        self.data_nascita.setDate(QDate.currentDate())

        self.attivo = QCheckBox("Attivo")
        self.attivo.setChecked(True)

        self.sesso = QComboBox()
        self.sesso.addItems(["Maschio", "Femmina", "Altro"])

        self.salva_btn = QPushButton("Salva")
        self.salva_btn.setStyleSheet(style_QButton_red)
        self.salva_btn.clicked.connect(self.submit_data)

        self.back_btn = QPushButton("Indietro")
        self.back_btn.setStyleSheet(style_QButton_white)
        self.back_btn.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.salva_btn)
        btn_container = QWidget()
        btn_container.setLayout(btn_layout)

        # Styling
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        layout.addRow("Nome:", self.nome)
        layout.addRow("Cognome:", self.cognome)
        layout.addRow("Username:", self.username)
        layout.addRow("Data di nascita:", self.data_nascita)
        layout.addRow("Stato:", self.attivo)
        layout.addRow("Sesso:", self.sesso)
        layout.addRow("", btn_container)

        self.setLayout(layout)


    def submit_data(self):
        if self.nome.text() == "" or self.cognome.text() == "":
            QMessageBox.warning(self, "Errore", "Nome e cognome sono obbligatori.")
            return
        self.data = {
            "nome": self.nome.text(),
            "cognome": self.cognome.text(),
            "username": self.username.text(),
            "data_nascita": self.data_nascita.date().toString("dd/MM/yyyy"),
            "attivo": self.attivo.isChecked(),
            "sesso": self.sesso.currentText()
        }
        #print("Dati inseriti:", data)
        QMessageBox.information(self, "Successo", "Dipendente aggiunto.")
        self.accept()
if __name__ == "__main__":
    from styles import *
    app = QApplication(sys.argv)
    window = add_Dipendete_ui()
    #window.resize(400, 300)
    window.exec()
else:
    from .styles import *