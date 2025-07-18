from typing import List

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTreeWidget, QTreeWidgetItem,
    QDateEdit, QComboBox, QFormLayout, QSplitter, QWidget
)
from View.styles import *
from View.topBar import topBar
from Model import Gender
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
    tree = QTreeWidget()
    tree.setHeaderLabels(
        ["Nome", "Cognome", "Data di Nascita", "Sesso", "Email", "Telefono","Id"])
    for player in player_list:
        item = QTreeWidgetItem([
            str(player.name),
            str(player.surname),
            str(player.birthday),
            str(player.gender.value),
            str(player.email),
            str(player.phone),
            str(player.id)
        ])
        tree.addTopLevelItem(item)
    tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    tree.setMaximumWidth(750)
    tree.setMinimumWidth(750)
    hSplitter.addWidget(tree)
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
    label_created_when = QLabel("Registrato il: -")
    label_created_when.setStyleSheet(style_text_gotham_b)

    label_created_by = QLabel("Registrato da: -")
    label_created_by.setStyleSheet(style_text_gotham_b)

    label_city = QLabel("Città: -")
    label_city.setStyleSheet(style_text_gotham_b)

    label_eta = QLabel("Prenotazioni: -")
    label_eta.setStyleSheet(style_text_gotham_b)

    label_time = QLabel("Orario Pref.: -")
    label_time.setStyleSheet(style_text_gotham_b)

    label_sport = QLabel("Sport Pref.: -")
    label_sport.setStyleSheet(style_text_gotham_b)

    label_avg_n_player = QLabel("Media pers/pren: -")
    label_avg_n_player.setStyleSheet(style_text_gotham_b)

    # Aggiungi al layout
    stats_layout.addWidget(label_name)
    stats_layout.addWidget(label_surname)
    stats_layout.addWidget(label_created_when)
    stats_layout.addWidget(label_created_by)
    stats_layout.addWidget(label_city)
    stats_layout.addWidget(label_eta)
    stats_layout.addWidget(label_time)
    stats_layout.addWidget(label_sport)
    stats_layout.addWidget(label_avg_n_player)
    stats_layout.setSpacing(12)
    stats_layout.addStretch()

    hSplitter.addWidget(stats_widget)
    # -------------------------------------------------------
    hSplitter.setCollapsible(0,False)
    hSplitter.setStretchFactor(0,0)
    hSplitter.setStretchFactor(1,1)
    hSplitter.handle(1).setEnabled(False)
    vLayout.addWidget(hSplitter)

    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)
    #--------------------- Search, Add, Del section-------------------------------------------------------
    btn_bar_widget = QWidget()
    btn_bar_widget.setFixedHeight(60)
    # add Player btn
    add_play_btn = QPushButton("Crea Giocatore")
    add_play_btn.setStyleSheet(style_QButton_white_18Gotham)
    add_play_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_play_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_play_btn = QPushButton("Elimina Giocatore")
    del_play_btn.setStyleSheet(style_QButton_disabled)
    del_play_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_play_btn.setEnabled(False)
    hLayoutBtn.addWidget(del_play_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    btn_bar_widget.setLayout(hLayoutBtn)
    #----------------------------------------------------------------------------

    vLayout.addWidget(btn_bar_widget)
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
    return main_layout, center_text, tree, label_name,label_surname,label_created_when,label_created_by,label_city,label_eta,label_time,label_sport,label_avg_n_player,add_play_btn, del_play_btn,back_btn

class info_Player_ui(QDialog):
    def __init__(self,phase:int,player_to_edit:Player=None,parent=None):
        #phase = 0 -> to register new Player
        #phase = 1 -> to edit an existing Player
        super().__init__(parent)
        self.phase = phase
        self.player_to_edit = player_to_edit
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
        genderCheck.addItems(["Maschio", "Femmina", "Altro"])

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
            date = self.player_to_edit.birthday.split("/")
            birth_day_sel.setDate(QDate(int(date[2]), int(date[1]), int(date[0])))
            print(type(self.player_to_edit.gender))
            genderCheck.setCurrentIndex(list(Gender.Gender).index(self.player_to_edit.gender))
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
            GENDER_MAP = {
                "Maschio": Gender.Gender.MALE,
                "Femmina": Gender.Gender.FEMALE,
                "Altro": Gender.Gender.OTHER
            }
            gender = GENDER_MAP.get(genderCheck.currentText(), Gender.Gender.OTHER)
            data = {
                "name": nameBar.text(),
                "surname": surnameBar.text(),
                "birthday": birth_day_sel.date().toString("dd/MM/yyyy"),
                "gender": gender,
                "phone":str(prefix_label.text())+" "+str(phoneBar.text()),
                "email":emailBar.text(),
                "city":cityBar.text()
            }
            # call his parent
            if self.phase==0:
                #REGISTER NEW PLAYER
                if hasattr(self.parent().players_controller, "register_player"):      #check if "self.register_dipendente" exists in 'MainWindow'"
                    success, err_id = self.parent().players_controller.register_player(list(data.values()),self.parent().users_controller.current_user)
                    if success:
                        self.parent().model.players_next_id = self.parent().players_controller.player_id
                        self.parent().model.save_to_file("data.pkl")
                        QMessageBox.information(self, "Successo", "Giocatore aggiunto.")
                        self.accept()
                    else:
                        # controller said: "no!"
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
                else:
                    QMessageBox.critical(self, "Errore", "Controller non valido/ha riscontrato un errore.")
            elif self.phase==1:
                #EDIT PLAYER
                if hasattr(self.parent().players_controller,"edit_player"):
                    success, err_id = self.parent().players_controller.edit_player(list(data.values()),self.player_to_edit.id)
                    if success:
                        self.parent().model.save_to_file("data.pkl")
                        QMessageBox.information(self, "Successo", f"Profilo di {self.player_to_edit.name} {self.player_to_edit.surname} modificato.")
                        self.accept()
                    else:
                        # controller said: "no!"
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
        save_btn.clicked.connect(submit_data)
        self.setLayout(main_layout)

if __name__ != "__main__":
    from .styles import *