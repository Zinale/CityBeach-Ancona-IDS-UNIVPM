import sys

from PyQt6.QtCore import QDate
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import *


class add_Dipendete_ui(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Dipendente")
        self.setFixedSize(300, 280)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        self.nameBar = QLineEdit()
        self.surnameBar = QLineEdit()
        self.usernameBar = QLineEdit()

        self.birth_day_sel = QDateEdit()
        self.birth_day_sel.setDisplayFormat("dd/MM/yyyy")
        self.birth_day_sel.setCalendarPopup(True)
        self.birth_day_sel.setDate(QDate.currentDate())

        self.flagAmministratore = QCheckBox("Amministratore")
        self.flagAmministratore.setChecked(False)

        self.genderCheck = QComboBox()
        self.genderCheck.addItems(["Maschio", "Femmina", "Altro"])

        self.save_btn = QPushButton("Salva")
        self.save_btn.setStyleSheet(style_QButton_red)
        self.save_btn.clicked.connect(self.submit_data)

        self.back_btn = QPushButton("Indietro")
        self.back_btn.setStyleSheet(style_QButton_white)
        self.back_btn.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.save_btn)

        # Styling
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        layout.addRow("Nome:", self.nameBar)
        layout.addRow("Cognome:", self.surnameBar)
        layout.addRow("Username:", self.usernameBar)
        layout.addRow("Data di nascita:", self.birth_day_sel)
        layout.addRow("Amministratore:", self.flagAmministratore)
        layout.addRow("Sesso:", self.genderCheck)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

    def submit_data(self):
        data = {
            "name": self.nameBar.text(),
            "surname": self.surnameBar.text(),
            "username": self.usernameBar.text(),
            "birthday": self.birth_day_sel.date().toString("dd/MM/yyyy"),
            "is_admin": self.flagAmministratore.isChecked(),
            "gender": self.genderCheck.currentText()
        }
        # call his parent
        if hasattr(self.parent().users_controller, "register"):      #check if "self.register_dipendente" exists in 'MainWindow'"
            success, err_id = self.parent().users_controller.register(self.nameBar.text(),self.surnameBar.text(),self.usernameBar.text(),
                                                     self.birth_day_sel.date().toString("dd/MM/yyyy"),self.flagAmministratore.isChecked(),
                                                     self.genderCheck.currentText())
            #print(err_id)
            if success:
                self.data = data
                QMessageBox.information(self, "Successo", "Dipendente aggiunto.")
                #print("REGISTRATO: ",self.data)
                self.accept()
            else:
                # controller said: "no!"
                if err_id == 1:
                    QMessageBox.warning(self, "Errore", "Il Nome non può contenere caratteri speciali")
                elif err_id == 2:
                    QMessageBox.warning(self, "Errore", "Il Cognome non può contenere caratteri speciali")
                elif err_id == 3:
                    QMessageBox.warning(self, "Errore", "Username già in uso")
                elif err_id == 2:
                    QMessageBox.warning(self, "Errore", "Username non può contenere caratteri speciali")
                elif err_id == 5:
                    QMessageBox.warning(self, "Errore", "Impossibile inserire una data pari o successiva alla corrente")
                elif err_id == -1:
                    QMessageBox.critical(self, "Errore", "Errore")
        else:
            QMessageBox.critical(self, "Errore", "Controller non valido.")
class edit_user_ui(QDialog):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifica Utente")
        self.setFixedSize(300, 300)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.current_user = self.parent().users_controller.get_current_user()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        nameBar = QLineEdit()
        nameBar.setText(self.current_user.name)
        surnameBar = QLineEdit()
        surnameBar.setText(self.current_user.surname)
        usernameBar = QLineEdit()
        usernameBar.setText(self.current_user.username)
        passwordBar = QLineEdit()
        passwordBar.setText(self.current_user.password)

        date = self.current_user.birthday.split("/")
        birth_day_sel = QDateEdit()
        birth_day_sel.setDisplayFormat("dd/MM/yyyy")
        birth_day_sel.setCalendarPopup(True)
        birth_day_sel.setDate(QDate(int(date[2]),int(date[1]),int(date[0])))

        flagAmministratore = QCheckBox("Amministratore")
        flagAmministratore.setChecked(self.current_user.is_admin)
        flagAmministratore.setEnabled(False)

        genderCheck = QComboBox()
        genderCheck.addItems(["Maschio", "Femmina", "Altro"])

        save_btn = QPushButton("Salva")
        save_btn.setStyleSheet(style_QButton_red)

        back_btn = QPushButton("Indietro")
        back_btn.setStyleSheet(style_QButton_white)
        back_btn.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(save_btn)

        # Styling
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        layout.addRow("Nome:", nameBar)
        layout.addRow("Cognome:", surnameBar)
        layout.addRow("Username:", usernameBar)
        layout.addRow("Password:",passwordBar)
        layout.addRow("Data di nascita:", birth_day_sel)
        layout.addRow("Amministratore:", flagAmministratore)
        layout.addRow("Sesso:", genderCheck)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        def submit_data():
            if hasattr(self.parent().users_controller,"edit_user"):  # check if "self.register_dipendente" exists in 'MainWindow'"
                success, err_id = self.parent().users_controller.edit_user(nameBar.text(), surnameBar.text(),
                                                                 usernameBar.text(),
                                                                 passwordBar.text(),
                                                                 birth_day_sel.date().toString("dd/MM/yyyy"),
                                                                 genderCheck.currentText())
                if success:
                    QMessageBox.information(self, "Successo", "Utente modificato.")
                    self.accept()
                else:
                    # controller said: "no!"
                    if err_id == 0:
                        QMessageBox.critical(self, "Errore", "Errore")
                    elif err_id == 1:
                        QMessageBox.warning(self, "Errore", "Il Nome non può contenere caratteri speciali")
                    elif err_id == 2:
                        QMessageBox.warning(self, "Errore", "Il Cognome non può contenere caratteri speciali")
                    elif err_id == 3:
                        QMessageBox.warning(self, "Errore", "Username già in uso")
                    elif err_id == 2:
                        QMessageBox.warning(self, "Errore", "Username non può contenere caratteri speciali")
                    elif err_id == 5:
                        QMessageBox.warning(self, "Errore",
                                            "Impossibile inserire una data pari o successiva alla corrente")
                    elif err_id == 6:
                        QMessageBox.warning(self, "Errore",
                                            "Impossibile modificare l'account 'admin'")
            else:
                QMessageBox.critical(self, "Errore", "Controller non valido.")
        save_btn.clicked.connect(submit_data)
        self.setLayout(main_layout)

if __name__ == "__main__":
    class Utente:
        pass
    from styles import *
    app = QApplication(sys.argv)
    window = add_Dipendete_ui()
    #window.resize(400, 300)
    window.exec()
else:
    from Model import *
    from .styles import *