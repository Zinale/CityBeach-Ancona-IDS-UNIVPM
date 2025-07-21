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
from Model.Field import Field
from Model.Locker import Locker
from Model.Player import Player
from Model.SportsCategory import SportsCategory
from Model.User import User
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
    if booking_list!=None:
        booking_list.reverse()
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
    def __init__(self,bookingController:AppBookingsController,fields_list:List[Field],
                 lockers_list:List[Locker],players_list:List[Player],currentUser:User=None):
        super().__init__()
        self.bookingsController = bookingController
        self.fieldsList = fields_list
        self.lockersList = lockers_list
        self.playersList = players_list
        self.currentUser = currentUser
        self.setWindowTitle("Crea Prenotazione")
        self.setFixedSize(450, 420)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        sportBox = QComboBox()
        sportBox.addItems([sport.value for sport in SportsCategory])
        fieldBox = QComboBox()
        fieldBox.addItems([field.name for field in self.fieldsList if field.sport==sportBox.currentText()])
        def update_field_box():
            fieldBox.clear()
            fieldBox.addItems([field.name for field in self.fieldsList if field.sport==sportBox.currentText()])
        sportBox.currentTextChanged.connect(update_field_box)

        names = list(set(player.name for player in self.playersList))
        surnames = list(set(player.surname for player in self.playersList))
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

        usrCheckPhone = QComboBox()
        usrCheckEmail = QComboBox()
        usrCheckBirthday = QComboBox()

        def checkUserInfo():
            name = playerName.text().strip()
            surname = playerSurname.text().strip()
            usrCheckPhone.clear()
            usrCheckEmail.clear()
            usrCheckBirthday.clear()
            if not name or not surname:
                return  # Se uno dei due è vuoto, non aggiungiamo nulla
            matching_players = [ply for ply in self.playersList if ply.name == name and ply.surname == surname]
            if matching_players:
                usrCheckPhone.addItems([ply.phone for ply in matching_players])
                usrCheckEmail.addItems([ply.email for ply in matching_players])
                usrCheckBirthday.addItems([str(ply.birthday) for ply in matching_players])
        playerName.textChanged.connect(checkUserInfo)
        playerSurname.textChanged.connect(checkUserInfo)
        nameCompleter.activated.connect(checkUserInfo)
        surnameCompleter.activated.connect(checkUserInfo)

        def updateCheckerComboBox():
            sender = self.sender()
            if sender==usrCheckEmail:
                usrCheckPhone.blockSignals(True)
                usrCheckPhone.setCurrentIndex(usrCheckEmail.currentIndex())
                usrCheckPhone.blockSignals(False)
                usrCheckBirthday.blockSignals(True)
                usrCheckBirthday.setCurrentIndex(usrCheckEmail.currentIndex())
                usrCheckBirthday.blockSignals(False)
            if sender==usrCheckPhone:
                usrCheckEmail.blockSignals(True)
                usrCheckEmail.setCurrentIndex(usrCheckPhone.currentIndex())
                usrCheckEmail.blockSignals(False)
                usrCheckBirthday.blockSignals(True)
                usrCheckBirthday.setCurrentIndex(usrCheckPhone.currentIndex())
                usrCheckBirthday.blockSignals(False)
            if sender==usrCheckBirthday:
                usrCheckPhone.blockSignals(True)
                usrCheckPhone.setCurrentIndex(usrCheckBirthday.currentIndex())
                usrCheckPhone.blockSignals(False)
                usrCheckEmail.blockSignals(True)
                usrCheckEmail.setCurrentIndex(usrCheckBirthday.currentIndex())
                usrCheckEmail.blockSignals(False)

        usrCheckEmail.currentTextChanged.connect(updateCheckerComboBox)
        usrCheckPhone.currentTextChanged.connect(updateCheckerComboBox)
        usrCheckBirthday.currentTextChanged.connect(updateCheckerComboBox)


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
        layout.addRow("Verifica numero Telefono:",usrCheckPhone)
        layout.addRow("Verifica numero E-mail:",usrCheckEmail)
        layout.addRow("Verifica data di nascita:",usrCheckBirthday)
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
            player =  next((player for player in self.playersList
                            if player.name == playerName.text() and player.surname==playerSurname.text()
                            and player.birthday==usrCheckBirthday.currentText() and player.email==usrCheckEmail.currentText()
                            and player.email==usrCheckEmail.currentText()),None)

            data = {
                "sport": sportBox.currentText(),
                "field": fieldBox.currentText(),
                "player": player,
                "nPlayer":nPlayer.value(),
                "nMale":nMale.value(),
                "nFemale":nFemale.value(),
                "price":price.value(),
                "date": date_selector.date().toString("dd/MM/yyyy"),
                "timeSlot": slot_selector.value(),
            }
            # call his parent
            try:
                success, err_id = self.bookingsController.register_booking(data,self.currentUser)
                if success:
                    QMessageBox.information(self, "Successo", "Dipendente aggiunto.")
                    #print("REGISTRATO: ",data)
                    self.accept()
                else:
                    # the controller said: "no!"
                    if err_id!=-1:
                        error_messages = {
                            1: "Nome non valido.",
                            2: "Tipo Attrezzatura non valido.",
                            3: "Categoria Sportiva non valida.",
                            4: "Quantità deve essere maggiore di zero."
                        }
                        QMessageBox.warning(self, "Errore", error_messages.get(err_id, "Errore sconosciuto."))
                    else:
                        QMessageBox.critical(self, "Errore", "Errore")
            except:
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
    from Model import *
    #from .Model import Gender
    from .styles import *
    from Model.SportsCategory import *