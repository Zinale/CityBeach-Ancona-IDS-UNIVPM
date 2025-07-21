from typing import List

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTreeWidget, QTreeWidgetItem,
    QDateEdit, QComboBox, QFormLayout, QCompleter, QSpinBox
)

from Controller import AppBookingsController
from Model.Data import TIME_SLOTS
import View.View
from Model.Booking import Booking
from Model.SportsCategory import SportsCategory
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

    del_book_btn = QPushButton("Annulla Prenotazione")
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

class add_booking_ui(QDialog):
    def __init__(self,controller:AppBookingsController,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crea Prenotazione")
        self.setFixedSize(450, 380)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        sportBox = QComboBox()
        sportBox.addItems([sport.value for sport in SportsCategory])
        fieldBox = QComboBox()
        if not hasattr(self.parent().fields_controller,"fields"):
            self.close()
        fieldBox.addItems([field.name for field in list(self.parent().fields_controller.fields.values()) if field.sport==sportBox.currentText()])
        if not hasattr(self.parent().players_controller,"players"):
            self.close()
        def update_field_box():
            fieldBox.clear()
            fieldBox.addItems([field.name for field in list(self.parent().fields_controller.fields.values()) if field.sport==sportBox.currentText()])
        sportBox.currentTextChanged.connect(update_field_box)

        names = [player.name for player in list(self.parent().players_controller.players.values())]
        surnames = [player.surname for player in list(self.parent().players_controller.players.values())]
        playerName = QLineEdit()
        playerName.setPlaceholderText("Inserisci nome Giocatore")
        nameCompleter = QCompleter(names,self)
        nameCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        playerName.setCompleter(nameCompleter)

        playerSurname = QLineEdit()
        playerSurname.setPlaceholderText("Inserisci cognome Giocatore")
        surnameCompleter = QCompleter(surnames,self)
        surnameCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        playerSurname.setCompleter(surnameCompleter)

        nPlayer = QSpinBox()
        nPlayer.setRange(0, 12)
        nPlayer.setValue(0)
        nMale = QSpinBox()
        nMale.setRange(0, 12)
        nMale.setValue(0)
        nFemale = QSpinBox()
        nFemale.setRange(0, 12)
        nFemale.setValue(0)
        def check_values():
            total = nPlayer.value()
            male = nMale.value()
            female = nFemale.value()
            if male + female > total:
                sender = self.sender()
                if sender == nMale:
                    nMale.blockSignals(True)
                    nMale.setValue(max(0, total - nFemale.value()))
                    nMale.blockSignals(False)
                elif sender == nFemale:
                    nFemale.blockSignals(True)
                    nFemale.setValue(max(0, total - nMale.value()))
                    nFemale.blockSignals(False)
                else:
                    nMale.blockSignals(True)
                    nFemale.blockSignals(True)
                    nMale.setValue(0)
                    nFemale.setValue(0)
                    nMale.blockSignals(False)
                    nFemale.blockSignals(False)
        nPlayer.valueChanged.connect(check_values)
        nMale.valueChanged.connect(check_values)
        nFemale.valueChanged.connect(check_values)

        price = QSpinBox()
        price.setRange(0,200)
        price.setValue(50)

        date_selector = QDateEdit()
        date_selector.setDisplayFormat("dd/MM/yyyy")
        date_selector.setCalendarPopup(True)
        date_selector.setDate(QDate.currentDate())

        slot_selector = QSpinBox()
        slot_selector.setRange(0,25)
        label_slot = QLabel(f"{TIME_SLOTS[slot_selector.value()].startTime}-{TIME_SLOTS[slot_selector.value()+2].endTime}")
        def update_label_slot():
            label_slot.setText(f"{TIME_SLOTS[slot_selector.value()].startTime}-{TIME_SLOTS[slot_selector.value()+2].endTime}")
        slot_selector.valueChanged.connect(update_label_slot)

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

        layout.addRow("Sport:", sportBox)
        layout.addRow("Campo:", fieldBox)
        layout.addRow("Nome Giocatore:", playerName)
        layout.addRow("Cognome Giocatore:", playerSurname)
        hLayout_nPlayer = QHBoxLayout()
        hLayout_nPlayer.addWidget(nPlayer)
        hLayout_nPlayer.addWidget(nMale)
        hLayout_nPlayer.addWidget(nFemale)
        layout.addRow("n° Giocatori/Maschi/Femmine:", hLayout_nPlayer)
        layout.addRow("Prezzo €:", price)
        layout.addRow("Data:", date_selector)
        hLayout_slot = QHBoxLayout()
        hLayout_slot.addWidget(slot_selector)
        hLayout_slot.addWidget(label_slot)
        layout.addRow("Fascia oraria:", hLayout_slot)


        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)







        def submit_data():
            #@TODO
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
    from Model.SportsCategory import *