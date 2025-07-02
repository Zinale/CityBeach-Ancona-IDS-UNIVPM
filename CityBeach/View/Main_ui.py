import sys

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTreeWidget, QTreeWidgetItem,
    QDateEdit, QComboBox, QCheckBox, QFormLayout, QGridLayout
)

from Model.User import User
from View.styles import *
from View.topBar import topBar
from Model import Gender

def main_ui_layout() -> QVBoxLayout() and QPushButton()and QPushButton()and QPushButton()and QPushButton()and QLabel()and QPushButton()and QPushButton():
    # Layout verticale principale
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    # --- TOP BAR ------------------------------------------------------------------------------------
    main_layout.addLayout(topBar())
    # --- Core: 2 row x 3 button with text ------------------------------------------------------------------------------------
    core_layout = QGridLayout()
    core_layout.setHorizontalSpacing(40)  # column space
    core_layout.setVerticalSpacing(20)  # row space

    vv1 = QVBoxLayout()
    vv2 = QVBoxLayout()
    vv3 = QVBoxLayout()
    vv4 = QVBoxLayout()
    vv5 = QVBoxLayout()
    vv6 = QVBoxLayout()
    # imgCampi = QIcon(QPixmap("src/img/Baby.tux.sit-800x800.png"))
    try:
        imgPrenotazioni = QIcon(QPixmap(image_path("1-1.jpg")))
        imgGiocatori = QIcon(QPixmap(image_path("1-1.jpg")))
        imgAttSpo = QIcon(QPixmap(image_path("1-1.jpg")))
        imgDipend = QIcon(QPixmap(image_path("1-1.jpg")))
        imgRisto = QIcon(QPixmap(image_path("1-1.jpg")))
    except:
        pass
    # CAMPI DA GIOCO
    btn_campi = QPushButton()
    btn_campi.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    # btn_campi.setIcon(imgCampi)
    # btn_campi.setIconSize(btn_campi.size())
    btn_campi.setStyleSheet(style_img1_bg("Baby.tux.sit-800x800.png"))
    label_campi = QLabel("Campi da Gioco - Spogliatoi")
    label_campi.setStyleSheet(style_text_gotham_b)
    label_campi.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    vv1.addWidget(btn_campi)
    vv1.addWidget(label_campi)
    vv1.setSpacing(6)
    core_layout.addLayout(vv1, 0, 0)
    # PRENOTAZIONE
    btn_pren = QPushButton()
    btn_pren.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    btn_pren.setStyleSheet(style_img1_bg("Baby.tux.sit-800x800.png"))
    label_pren = QLabel("Prenotazioni")
    label_pren.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    label_pren.setStyleSheet(style_text_gotham_b)
    vv2.addWidget(btn_pren)
    vv2.addWidget(label_pren)
    vv2.setSpacing(6)
    core_layout.addLayout(vv2, 0, 1)
    # Profili Giocatori
    btn_gioc = QPushButton()
    btn_gioc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    btn_gioc.setStyleSheet(style_img1_bg("Baby.tux.sit-800x800.png"))
    label_gioc = QLabel("Profili Giocatori")
    label_gioc.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    label_gioc.setStyleSheet(style_text_gotham_b)
    vv3.addWidget(btn_gioc)
    vv3.addWidget(label_gioc)
    vv3.setSpacing(6)
    core_layout.addLayout(vv3, 0, 2)

    # Att. Sportiva
    btn_attspo = QPushButton()
    btn_attspo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    btn_attspo.setStyleSheet(style_img1_bg("Baby.tux.sit-800x800.png"))
    label_attspo = QLabel("Attrezzatura Sportiva")
    label_attspo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    label_attspo.setStyleSheet(style_text_gotham_b)
    vv4.addWidget(btn_attspo)
    vv4.addWidget(label_attspo)
    vv4.setSpacing(6)
    core_layout.addLayout(vv4, 1, 0)

    btn_dip = QPushButton()
    btn_dip.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    btn_dip.setStyleSheet(style_img1_bg("Baby.tux.sit-800x800.png"))
    #btn_dip.clicked.connect(view_dipendenti)
    label_dip = QLabel("Dipendenti")
    label_dip.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    label_dip.setStyleSheet(style_text_gotham_b)
    vv5.addWidget(btn_dip)
    vv5.addWidget(label_dip)
    vv5.setSpacing(6)
    core_layout.addLayout(vv5, 1, 1)

    # Area Ristoro
    btn_rist = QPushButton()
    btn_rist.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    btn_rist.setStyleSheet(style_img1_bg("Baby.tux.sit-800x800.png"))
    label_rist = QLabel("Area ristoro")
    label_rist.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    label_rist.setStyleSheet(style_text_gotham_b)
    vv6.addWidget(btn_rist)
    vv6.addWidget(label_rist)
    vv6.setSpacing(6)
    core_layout.addLayout(vv6, 1, 2)

    # Permette al layout centrale di espandersi
    for col in range(3):
        core_layout.setColumnStretch(col, 1)
    for row in range(2):
        core_layout.setRowStretch(row, 1)

    main_layout.addLayout(core_layout, stretch=1)

    # --- BOTTOM BAR ------------------------------------------------------------------------------------
    bottom_bar = QHBoxLayout()
    bottom_bar.setContentsMargins(0, 0, 0, 0)

    # Logo piccolo (24px di altezza)
    # DA FARE PER TUTTE LE IMMAGINI
    logo_label = QLabel()
    try:
        pixmap = QPixmap(image_path("logo.png"))
        if not pixmap.isNull():
            logo_label.setPixmap(
                pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
            )
    except Exception as e:
        print(f"Errore caricamento immagine: {e}")

    bottom_bar.addWidget(logo_label)
    bottom_bar.addSpacing(10)

    # Testo centrale            #f"{self.controller.get_current_user().username}"
    center_text = QLabel()
    center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
    #if not self.controller.get_current_user().is_admin:
    #    center_text.setStyleSheet(style_text_red_on_white)
    #else:
    #    center_text.setStyleSheet(style_text_white_on_red)

    bottom_bar.addStretch()
    bottom_bar.addWidget(center_text)

    profile_btn = QPushButton("Visualizza Profilo")
    profile_btn.setStyleSheet(style_QButton_white)
    #profile_btn.clicked.connect(show_edit_user_ui)
    bottom_bar.addWidget(profile_btn)

    log_btn = QPushButton("Logout")
    log_btn.setStyleSheet(style_QButton_red)
    #log_btn.clicked.connect(self.logout)
    bottom_bar.addWidget(log_btn)

    main_layout.addLayout(bottom_bar)
    return main_layout, btn_campi, btn_pren,btn_gioc,btn_attspo,btn_dip,btn_rist,center_text,profile_btn,log_btn

class edit_user_ui(QDialog):
    def __init__(self,opener_id:int,user_to_edit:User=None,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modifica Utente")
        self.setFixedSize(300, 300)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.current_user = self.parent().users_controller.get_current_user()
        self.opener_is_admin = False
        self.user_to_edit = self.current_user
        if self.current_user.id != user_to_edit.id:
            self.opener_is_admin = True
            self.user_to_edit = user_to_edit
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        nameBar = QLineEdit()
        nameBar.setText(self.user_to_edit.name)
        surnameBar = QLineEdit()
        surnameBar.setText(self.user_to_edit.surname)
        usernameBar = QLineEdit()
        usernameBar.setText(self.user_to_edit.username)
        if self.opener_is_admin:
            passwordBar = QCheckBox()
        else:
            passwordBar = QLineEdit()

        date = self.user_to_edit.birthday.split("/")
        birth_day_sel = QDateEdit()
        birth_day_sel.setDisplayFormat("dd/MM/yyyy")
        birth_day_sel.setCalendarPopup(True)
        birth_day_sel.setDate(QDate(int(date[2]),int(date[1]),int(date[0])))

        flagAmministratore = QCheckBox("Amministratore")
        flagAmministratore.setChecked(self.user_to_edit.is_admin)
        flagAmministratore.setEnabled(False)

        genderCheck = QComboBox()
        genderCheck.addItems(["Maschio", "Femmina", "Altro"])
        genderCheck.setCurrentIndex(list(Gender.Gender).index(self.user_to_edit.gender))

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
        if self.opener_is_admin:
            layout.addRow("Reset Password:",passwordBar)
        else:
            layout.addRow("Password:",passwordBar)
        layout.addRow("Data di nascita:", birth_day_sel)
        layout.addRow("Amministratore:", flagAmministratore)
        layout.addRow("Sesso:", genderCheck)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        def submit_data():
            GENDER_MAP = {
                "Maschio": Gender.Gender.MALE,
                "Femmina": Gender.Gender.FEMALE
            }
            gender = GENDER_MAP.get(genderCheck.currentText(), Gender.Gender.OTHER)
            if hasattr(self.parent().users_controller,"edit_user"):  # check if "self.register_dipendente" exists in 'MainWindow'"
                if self.opener_is_admin:
                    passwordVal = passwordBar.isChecked()
                else:
                    passwordVal = passwordBar.text()
                success, err_id = self.parent().users_controller.edit_user(self.user_to_edit.id,nameBar.text(), surnameBar.text(),
                                                                 usernameBar.text(),
                                                                 passwordVal,
                                                                 birth_day_sel.date().toString("dd/MM/yyyy"),
                                                                 gender)
                if success:
                    self.parent().model.save_to_file("data.pkl")
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
