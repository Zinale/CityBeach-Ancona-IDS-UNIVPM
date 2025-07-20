from typing import List

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTreeWidget, QTreeWidgetItem,
    QDateEdit, QComboBox, QCheckBox, QFormLayout
)

from Model.Booking import Booking
from View.styles import *
from View.topBar import topBar
from Model import Gender


def view_booking_ui_layout(booking_list:List[Booking]):
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    vLayout = QVBoxLayout()
    # --- TOP BAR ------------------------------------------------------------------------------------
    main_layout.addLayout(topBar())
    # --- Text + QTreeWidget + Add / ------------------------------------------------------------------------------------
    contextText = QLabel("Lista Prenotazioni:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignCenter)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;""")
    vLayout.addWidget(contextText)

    tree = QTreeWidget()
    tree.setHeaderLabels(
        ["Numero", "Sport", "Campo", "Giocatore", "#Giocatori", "Costo", "Data", "Fascia Oraria",
         "Registrata il","Stato Prenotazione","Registrata da"])
    for bk in booking_list:
        item = QTreeWidgetItem([
            str(bk.id),
            str(bk.field.sport),
            str(bk.field.name),
            str(bk.player.name + " " +bk.player.surname),
            str(bk.totalPlayers),
            str(bk.price),
            str(bk.time.day),
            str(bk.time.getAllTime()),
            str(bk.data_created.date()),
            str(bk.state),
            str(bk.registered_by.username)
        ])
        tree.addTopLevelItem(item)

    vLayout.addWidget(tree)
    tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)
    # add Bookin btn
    book_btn = QPushButton("Crea Prenotazione")
    book_btn.setStyleSheet(style_QButton_white_18Gotham)
    book_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(book_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_book_btn = QPushButton("Elimina Prenotazione")
    del_book_btn.setStyleSheet(style_QButton_white_18Gotham)
    del_book_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(del_book_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

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
    return main_layout,center_text, tree, book_btn, del_book_btn,back_btn

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
        layout.addRow("Data di nascita:", birth_day_sel)
        layout.addRow("Amministratore:", flagAmministratore)
        layout.addRow("Sesso:", genderCheck)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        def submit_data():
            GENDER_MAP = {
                "Maschio": Gender.Gender.MALE,
                "Femmina": Gender.Gender.FEMALE
            }
            gender = GENDER_MAP.get(genderCheck.currentText(), Gender.Gender.OTHER)
            data = {
                "name": nameBar.text(),
                "surname": surnameBar.text(),
                "username": usernameBar.text(),
                "birthday": birth_day_sel.date().toString("dd/MM/yyyy"),
                "is_admin": flagAmministratore.isChecked(),
                "gender": gender
            }
            # call his parent
            if hasattr(self.parent().users_controller, "register"):      #check if "self.register_dipendente" exists in 'MainWindow'"
                success, err_id = self.parent().users_controller.register(nameBar.text(),surnameBar.text(),usernameBar.text(),
                                                         birth_day_sel.date().toString("dd/MM/yyyy"),flagAmministratore.isChecked(),
                                                         gender)
                if success:
                    data = data
                    self.parent().model.users_next_id = self.parent().users_controller.user_id
                    self.parent().model.save_to_file("data.pkl")
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
                    elif err_id == -1:
                        QMessageBox.critical(self, "Errore", "Errore")
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
    #from .Model import Gender
    from .styles import *