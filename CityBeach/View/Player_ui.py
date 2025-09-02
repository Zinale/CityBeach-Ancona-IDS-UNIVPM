from typing import List

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QMessageBox,
    QDateEdit, QComboBox, QFormLayout, QSplitter, QWidget, QCheckBox, QTableWidget, QTableWidgetItem, QHeaderView
)

from Controller import AppPlayersController
from Model.User import User
from View.styles import *
from View.topBar import topBar
from Model.Gender import Gender
from Model import Player

def view_players_ui_layout(player_list: List[Player]):
    # Layout verticale principale
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    vLayout = QVBoxLayout()
    # --- TOP BAR ------------------------------------------------------------------------------------
    top_bar_widget = QWidget()
    top_bar_widget.setFixedHeight(21)
    top_bar_widget.setLayout(topBar())
    main_layout.addWidget(top_bar_widget)
    # --- Text + QTreeWidget + Add / ------------------------------------------------------------------------------------
    contextText = QLabel("Lista Giocatori:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignCenter)
    contextText.setFixedHeight(23)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;""")
    vLayout.addWidget(contextText)
    hSplitter = QSplitter(Qt.Orientation.Horizontal)

    # ----------------- TREE WIDGET ----------------
    table = QTableWidget()
    def populateTable():
        players = []
        table.clear()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(
            ["Nome", "Cognome", "Data di Nascita", "Sesso", "Email", "Telefono", "Id"])
        #filters
        name_surname = None
        email = None
        phone = None
        if byNameCheckBox.isChecked():
            name_surname = byNameLine.text()
        if byEmailCheckBox.isChecked():
            email = byEmailLine.text()
        if byPhoneCheckBox.isChecked():
            phone = byPhoneLine.text().strip()
        for player in player_list:
            if (name_surname and name_surname not in f"({player.name} {player.surname})") or (phone and phone not in player.phone) or (email and email not in player.email):
                continue
            players.append(player)
        table.setRowCount(len(players))
        for row, player in enumerate(players):
            values =([
                str(player.name),
                str(player.surname),
                str(player.birthday.strftime("%d/%m/%Y")),
                str(player.gender.value),
                str(player.email),
                str(player.phone),
                str(player.id)
            ])
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                table.setItem(row, col, item)

    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    table.setMaximumWidth(750)
    table.setMinimumWidth(750)
    hSplitter.addWidget(table)
    #-------------------------------------------------------
    #--------------Player Stats------------------------------
    stats_widget = QWidget()
    stats_layout = QVBoxLayout(stats_widget)
    stats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    stats_layout.setContentsMargins(10, 10, 10, 10)

    label_name = QLabel("Nome")
    label_name.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;font-weight: bold;""")
    label_surname = QLabel("Cognome")
    label_surname.setStyleSheet("""font-family: Gotham; color: #E30613;font-size: 20pt;font-weight: bold;""")
    # Etichette vuote che verranno aggiornate dinamicamente
    label_eta = QLabel("Età: -")
    label_eta.setStyleSheet(style_text_gotham_b)

    label_created_when = QLabel("Registrato il: -")
    label_created_when.setStyleSheet(style_text_gotham_b)

    label_created_by = QLabel("Registrato da: -")
    label_created_by.setStyleSheet(style_text_gotham_b)

    label_city = QLabel("Città: -")
    label_city.setStyleSheet(style_text_gotham_b)

    label_bookings = QLabel("Prenotazioni: -")
    label_bookings.setStyleSheet(style_text_gotham_b)

    label_book_lastMonth = QLabel("Pren. questo mese: -")
    label_book_lastMonth.setStyleSheet(style_text_gotham_b)

    label_fav_time = QLabel("Orario Pref.: -")
    label_fav_time.setStyleSheet(style_text_gotham_b)

    label_fav_sport = QLabel("Sport Pref.: -")
    label_fav_sport.setStyleSheet(style_text_gotham_b)

    label_avg_n_player = QLabel("Media pers/pren: -")
    label_avg_n_player.setStyleSheet(style_text_gotham_b)

    # Aggiungi al layout
    stats_layout.addWidget(label_name)
    stats_layout.addWidget(label_surname)
    stats_layout.addWidget(label_eta)
    stats_layout.addWidget(label_created_when)
    stats_layout.addWidget(label_created_by)
    stats_layout.addWidget(label_city)
    stats_layout.addWidget(label_bookings)
    stats_layout.addWidget(label_book_lastMonth)
    stats_layout.addWidget(label_fav_time)
    stats_layout.addWidget(label_fav_sport)
    stats_layout.addWidget(label_avg_n_player)
    stats_layout.setSpacing(14)
    stats_layout.addStretch()

    hSplitter.addWidget(stats_widget)
    hSplitter.setCollapsible(0,False)
    hSplitter.setStretchFactor(0,0)
    hSplitter.setStretchFactor(1,1)
    hSplitter.handle(1).setEnabled(False)
    vLayout.addWidget(hSplitter)
    #--------Filter Title--------------------------------------------------------------
    hLayoutFiltBtn = QHBoxLayout()
    hLayoutFiltBtn.setContentsMargins(0, 0, 0, 0)
    hLayoutFiltBtn.setSpacing(20)
    labelTitle = QLabel("Filtra per")
    labelTitle.setStyleSheet(style_text_red_on_white)
    labelTitle.setFixedSize(145, 40)
    hLayoutFilterTitle = QHBoxLayout()
    hLayoutFilterTitle.addWidget(labelTitle)
    hLayoutFilterTitle.addStretch(1)
    vLayout.addLayout(hLayoutFilterTitle,stretch=0)
    #-----------------------
    # FILTER 1: Name
    byNameCheckBox = QCheckBox("Nome/Cognome:")
    byNameLine = QLineEdit()
    block1 = QWidget()
    bl1_layout = QHBoxLayout(block1)
    bl1_layout.setContentsMargins(0, 0, 0, 0)
    bl1_layout.setSpacing(3)
    bl1_layout.addWidget(byNameCheckBox)
    bl1_layout.addWidget(byNameLine)
    byNameCheckBox.setChecked(False)
    byNameLine.setEnabled(False)
    byNameCheckBox.checkStateChanged.connect(lambda :byNameLine.setEnabled(byNameCheckBox.isChecked()))
    byNameCheckBox.checkStateChanged.connect(populateTable)
    byNameLine.textChanged.connect(populateTable)
    # FILTER 2: Email
    byEmailCheckBox = QCheckBox("Email:")
    byEmailLine = QLineEdit()
    block2 = QWidget()
    bl2_layout = QHBoxLayout(block2)
    bl2_layout.setContentsMargins(0, 0, 0, 0)
    bl2_layout.setSpacing(3)
    bl2_layout.addWidget(byEmailCheckBox)
    bl2_layout.addWidget(byEmailLine)
    byEmailLine.setPlaceholderText("prova@esempio.it")
    byEmailCheckBox.setChecked(False)
    byEmailLine.setEnabled(False)
    byEmailCheckBox.checkStateChanged.connect(lambda :byEmailLine.setEnabled(byEmailCheckBox.isChecked()))
    byEmailCheckBox.checkStateChanged.connect(populateTable)
    byEmailLine.textChanged.connect(populateTable)
    # FILTER 1: Name
    byPhoneCheckBox = QCheckBox("Telefono:")
    byPhoneLine = QLineEdit()
    block3 = QWidget()
    bl3_layout = QHBoxLayout(block3)
    bl3_layout.setContentsMargins(0, 0, 0, 0)
    bl3_layout.setSpacing(3)
    bl3_layout.addWidget(byPhoneCheckBox)
    bl3_layout.addWidget(byPhoneLine)
    byPhoneLine.setInputMask("999 999 9999;_")
    byPhoneCheckBox.setChecked(False)
    byPhoneLine.setEnabled(False)
    byPhoneCheckBox.checkStateChanged.connect(lambda :byPhoneLine.setEnabled(byPhoneCheckBox.isChecked()))
    byPhoneCheckBox.checkStateChanged.connect(populateTable)
    byPhoneLine.textChanged.connect(populateTable)

    #add filters blocks to btns layout
    block1.setStyleSheet(style_app_Dialogs)
    block2.setStyleSheet(style_app_Dialogs)
    block3.setStyleSheet(style_app_Dialogs)
    hLayoutFiltBtn.addWidget(block1)
    hLayoutFiltBtn.addWidget(block2)
    hLayoutFiltBtn.addWidget(block3)
    hLayoutFiltBtn.addStretch(1)

    #--------------------- Search, Add, Del section-------------------------------------------------------
    # add Player btn
    add_play_btn = QPushButton("Crea Giocatore")
    add_play_btn.setStyleSheet(style_QButton_white_17Gotham)
    add_play_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutFiltBtn.addWidget(add_play_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_play_btn = QPushButton("Elimina Giocatore")
    del_play_btn.setStyleSheet(style_QButton_disabled)
    del_play_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_play_btn.setEnabled(False)
    hLayoutFiltBtn.addWidget(del_play_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    btnsWidget = QWidget()
    btnsWidget.setFixedHeight(40)
    btnsWidget.setLayout(hLayoutFiltBtn)
    #----------------------------------------------------------------------------

    vLayout.addWidget(btnsWidget)
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
    populateTable()
    return main_layout, center_text, table, label_name,label_surname,label_eta,label_created_when,label_created_by,label_city,label_bookings,label_book_lastMonth,label_fav_time,label_fav_sport,label_avg_n_player,add_play_btn, del_play_btn,back_btn

class info_Player_ui(QDialog):
    def __init__(self,phase:int,playerController:AppPlayersController,player_to_edit:Player=None,currentUser:User=None):
        #phase = 0 -> to register new Player
        #phase = 1 -> to edit an existing Player
        super().__init__()
        self.phase = phase
        self.playersController = playerController
        self.player_to_edit = player_to_edit
        self.currentUser = currentUser
        if phase==0:
            self.setWindowTitle("Aggiungi Giocatore")
        else:
            self.setWindowTitle(f"Modifica {player_to_edit.name} {player_to_edit.surname}")
        self.setFixedSize(300, 320)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        nameBar = QLineEdit()
        surnameBar = QLineEdit()

        birth_day_sel = QDateEdit()
        birth_day_sel.setDisplayFormat("dd/MM/yyyy")
        birth_day_sel.setCalendarPopup(True)
        birth_day_sel.setDate(QDate.currentDate())

        genderCheck = QComboBox()
        genderCheck.addItems([g.value for g in Gender])

        emailBar = QLineEdit()
        emailBar.setPlaceholderText("prova@esempio.it")
        cityBar = QLineEdit()

        phone_widget = QWidget()
        phone_layout = QHBoxLayout()
        phone_layout.setContentsMargins(0, 0, 0, 0)
        prefix_label = QLineEdit("+39")
        prefix_label.setPlaceholderText("+39")
        prefix_label.setMaximumWidth(40)
        phoneBar = QLineEdit()
        phoneBar.setInputMask("999 999 9999;_")
        phone_layout.addWidget(prefix_label)
        phone_layout.addWidget(phoneBar)
        phone_widget.setLayout(phone_layout)

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
        layout.addRow("Data di nascita:", birth_day_sel)
        layout.addRow("Sesso:", genderCheck)
        layout.addRow("Telefono: ",phone_widget)
        layout.addRow("Email: ",emailBar)
        layout.addRow("Città: ",cityBar)

        if self.phase == 1:
            nameBar.setText(f"{self.player_to_edit.name}")
            surnameBar.setText(f"{self.player_to_edit.surname}")
            #date = self.player_to_edit.birthday.split("/")
            birth_day_sel.setDate(self.player_to_edit.birthday)
            genderCheck.setCurrentIndex(list([g.value for g in Gender]).index(self.player_to_edit.gender.value))
            phone_number = self.player_to_edit.phone.split(" ")
            prefix_label.setText(phone_number[0])
            phoneBar.setText("".join(phone_number[1:]))
            emailBar.setText(self.player_to_edit.email)
            cityBar.setText(self.player_to_edit.residence)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        def submit_data():
            data = {
                "name": nameBar.text(),
                "surname": surnameBar.text(),
                "birthday": birth_day_sel.date().toString("dd/MM/yyyy"),
                "gender": Gender(genderCheck.currentText()),
                "phone":str(prefix_label.text())+" "+str(phoneBar.text()),
                "email":emailBar.text(),
                "city":cityBar.text()
            }
            # call his parent
            if self.phase==0:
                #REGISTER NEW PLAYER
                try:
                    success, err_id = self.playersController.register_player(data,self.currentUser)
                    if success:
                        QMessageBox.information(self, "Successo", "Giocatore aggiunto.")
                        self.accept()
                    else:
                        # the controller said: "no!"
                        if err_id == 1:
                            QMessageBox.warning(self, "Errore", "Impossibile inserire una data pari o successiva alla corrente")
                        elif err_id == 2:
                            QMessageBox.warning(self, "Errore", "Nessuno sta utilizzando il programma")
                        elif err_id == 3:
                            QMessageBox.warning(self, "Errore", "Email non vaida")
                        elif err_id == 4:
                            QMessageBox.warning(self, "Errore", "Email già usata")
                        elif err_id == 5:
                            QMessageBox.warning(self, "Errore", "Numero di telefono già usato")
                        elif err_id == -1:
                            QMessageBox.critical(self, "Errore", "Errore")
                except:
                    QMessageBox.critical(self, "Errore", "Controller non valido/ha riscontrato un errore.")
                    self.close()
            elif self.phase==1:
                #EDIT PLAYER
                try:
                    success, err_id = self.playersController.edit_player(list(data.values()),self.player_to_edit.id)
                    if success:
                        QMessageBox.information(self, "Successo", f"Profilo di {self.player_to_edit.name} {self.player_to_edit.surname} modificato.")
                        self.accept()
                    else:
                        # the controller said: "no!"
                        if err_id == 1:
                            QMessageBox.warning(self, "Errore", "Impossibile inserire una data pari o successiva alla corrente")
                        elif err_id == 2:
                            QMessageBox.warning(self, "Errore", "Email non vaida")
                        elif err_id == 3:
                            QMessageBox.warning(self, "Errore", "Email già usata")
                        elif err_id == 4:
                            QMessageBox.warning(self, "Errore", "Numero di telefono già usato")
                        elif err_id == -1:
                            QMessageBox.critical(self, "Errore", "Errore")
                except:
                    self.close()
        save_btn.clicked.connect(submit_data)
        self.setLayout(main_layout)

if __name__ != "__main__":
    from .styles import *