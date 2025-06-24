from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, \
    QMessageBox, QGridLayout

import sys
from View.Dialogs import edit_user_ui
from View.styles import style_img1_bg, style_text_gotham_b, style_QButton_white, style_QButton_red, \
    style_text_red_on_white, style_text_white_on_red
from View.topBar import topBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, \
    QMessageBox, QGridLayout, QTreeWidget, QTreeWidgetItem

import sys
from View.Dialogs import edit_user_ui
from View.styles import style_img1_bg, style_text_gotham_b, style_QButton_white, style_QButton_red, \
    style_text_red_on_white, style_text_white_on_red, style_QButton_white_18Gotham
from View.topBar import topBar
from paths import image_path


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
    label_campi = QLabel("Campi da Gioco")
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