import sys

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QDateEdit, QComboBox, QCheckBox, QFormLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from typing import List

from Controller import AppUsersController
from Model.User import User
from View.styles import *
from View.topBar import topBar
from Model.Gender import Gender


def view_dipendenti_ui_layout(lista_dipendenti):
    # Layout verticale principale
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    vLayout = QVBoxLayout()
    # --- TOP BAR ------------------------------------------------------------------------------------
    main_layout.addLayout(topBar())
    # --- Text + QTreeWidget + Add / ------------------------------------------------------------------------------------
    contextText = QLabel("Lista Dipendenti:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignCenter)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;""")
    vLayout.addWidget(contextText)

    table = QTableWidget()
    table.setColumnCount(9)
    table.setHorizontalHeaderLabels(
        ["Nome", "Cognome", "ID", "Amministratore", "Username",
         "Data di Nascita", "Sesso", "Creato il", "Creato da"]
    )
    visible_users = [u for u in lista_dipendenti if u.id != 1]      #not "root" user
    table.setRowCount(len(visible_users))

    for row, user in enumerate(visible_users):
        values = [
            str(user.name),
            str(user.surname),
            str(user.id),
            "Si" if user.is_admin else "No",
            str(user.username),
            str(user.birthday),
            str(user.gender.value),
            str(user.data_created),
            str(user.added_by)
        ]
        for col, val in enumerate(values):
            item = QTableWidgetItem(val)
            if user.is_admin:
                item.setBackground(QBrush(QColor("#E30613")))
                item.setForeground(QBrush(QColor("#ffffff")))
            item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            table.setItem(row, col, item)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    vLayout.addWidget(table)

    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)
    # add Dipendente btn
    dip_btn = QPushButton("Crea Dipendente")
    dip_btn.setStyleSheet(style_QButton_white_17Gotham)
    dip_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(dip_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_dip_btn = QPushButton("Elimina Dipendente")
    del_dip_btn.setStyleSheet(style_QButton_white_17Gotham)
    del_dip_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(del_dip_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    vLayout.addLayout(hLayoutBtn)
    vLayout.setSpacing(15)
    main_layout.addLayout(vLayout)

    # --- BOTTOM BAR ------------------------------------------------------------------------------------
    bottom_bar = QHBoxLayout()
    bottom_bar.setContentsMargins(0, 0, 0, 0)

    logo_label = QLabel()
    try:
        pixmap = QPixmap("src/img/logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(
                pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
            )
    except Exception as e:
        print(f"Errore caricamento immagine: {e}")

    bottom_bar.addWidget(logo_label)
    bottom_bar.addSpacing(10)

    # mid text
    #f"{self.controller.get_current_user().username}"
    center_text = QLabel()
    center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    bottom_bar.addStretch()
    bottom_bar.addWidget(center_text)
    bottom_bar.addStretch()

    # right btn
    back_btn = QPushButton("Indietro")
    back_btn.setStyleSheet(style_QButton_red)
    #back_btn.clicked.connect(self.init_main_ui)
    bottom_bar.addWidget(back_btn)
    main_layout.addLayout(bottom_bar)
    return main_layout,center_text, table, dip_btn, del_dip_btn,back_btn

def updateTableEmployees(table,users):
    table.clear()
    table.setColumnCount(9)
    table.setHorizontalHeaderLabels(
        ["Nome", "Cognome", "ID", "Amministratore", "Username",
         "Data di Nascita", "Sesso", "Creato il", "Creato da"]
    )
    visible_users = [u for u in users if u.id != 1]  # not "root" user
    table.setRowCount(len(visible_users))
    for row, user in enumerate(visible_users):
        values = [
            str(user.name),
            str(user.surname),
            str(user.id),
            "Si" if user.is_admin else "No",
            str(user.username),
            str(user.birthday),
            str(user.gender.value),
            str(user.data_created),
            str(user.added_by)
        ]
        for col, val in enumerate(values):
            item = QTableWidgetItem(val)
            if user.is_admin:
                item.setBackground(QBrush(QColor("#E30613")))
                item.setForeground(QBrush(QColor("#ffffff")))
            item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
            table.setItem(row, col, item)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    return table

class add_Dipendete_ui(QDialog):
    def __init__(self,controller:AppUsersController = None):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Aggiungi Dipendente")
        self.setFixedSize(300, 280)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        nameBar = QLineEdit()
        surnameBar = QLineEdit()
        usernameBar = QLineEdit()

        birth_day_sel = QDateEdit()
        birth_day_sel.setDisplayFormat("dd/MM/yyyy")
        birth_day_sel.setCalendarPopup(True)
        birth_day_sel.setDate(QDate.currentDate())

        flagAmministratore = QCheckBox("Amministratore")
        flagAmministratore.setChecked(False)

        genderCheck = QComboBox()
        genderCheck.addItems([g.value for g in Gender])
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
        layout.addRow("Data di nascita:", birth_day_sel)
        layout.addRow("Amministratore:", flagAmministratore)
        layout.addRow("Sesso:", genderCheck)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        def submit_data():
            data = {
                "name": nameBar.text(),
                "surname": surnameBar.text(),
                "username": usernameBar.text(),
                "birthday": birth_day_sel.date().toString("dd/MM/yyyy"),
                "is_admin": flagAmministratore.isChecked(),
                "gender": Gender(genderCheck.currentText())
            }
            try:
                success, err_id = self.controller.register(data)
                if success:
                    QMessageBox.information(self, "Successo", "Dipendente aggiunto.")
                    #print("REGISTRATO: ",data)
                    self.accept()
                else:
                    # the controller said: "no!"
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
                    elif err_id == 6:
                        QMessageBox.warning(self, "Errore", "Non sei un amministratore!")
                    elif err_id == -1:
                        QMessageBox.critical(self, "Errore", "Errore")
            except Exception:
                QMessageBox.critical(self, "Errore", "Controller non valido.")
                self.close()
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
    from .styles import *