from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QSplitter, QWidget
)
from View.styles import *
from View.topBar import topBar
from Model.Locker import Locker
from Model.Field import Field

def view_fields_lockers_static_ui_layout(field_list: List[Field],locker_list:List[Locker]):
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
    # --------STATIC vs DYNAMIC ------------------------------------------------------------------
    hStaDynBtnLayout = QHBoxLayout()
    hStaDynBtnLayout.addStretch(1)
    stat_btn = QPushButton("Statica")
    stat_btn.setStyleSheet(style_QButton_red)
    stat_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    stat_btn.setEnabled(False)
    hStaDynBtnLayout.addWidget(stat_btn)
    hStaDynBtnLayout.addSpacing(10)
    dyna_btn = QPushButton("Dinamica")
    dyna_btn.setStyleSheet(style_QButton_white)
    dyna_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    hStaDynBtnLayout.addWidget(dyna_btn)
    hStaDynBtnLayout.addStretch(1)
    hStaDynBtnWidget = QWidget()
    hStaDynBtnWidget.setLayout(hStaDynBtnLayout)
    hStaDynBtnWidget.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Fixed)
    vLayout.addWidget(hStaDynBtnWidget,alignment=Qt.AlignmentFlag.AlignCenter)
    # ---------------------------------------------------------------------------------------
    hSplitter = QSplitter(Qt.Orientation.Horizontal)
    #splitter per layout SINISTRA (testo + tree + testo + tree) + Destra
    vLeftLayout = QVBoxLayout()
    #---------------------------------------------------------------------------------------
    contextText = QLabel("Campi da Gioco:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignLeft)
    contextText.setFixedHeight(24)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 15pt;""")
    vLeftLayout.addWidget(contextText)
    # TREE WIDGET FIELD----------------
    treeFields = QTreeWidget()
    treeFields.setHeaderLabels(
        ["Nome", "id", "Sport", "Aggiunto da","Data aggiunto"])
    for field in field_list:
        item = QTreeWidgetItem([
            str(field.name),
            str(field.id),
            str(field.sport),
            str(field.added_by),
            str(field.data_created.date())
        ])
        treeFields.addTopLevelItem(item)
    treeFields.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    treeFields.setMaximumWidth(650)
    treeFields.setMinimumWidth(650)
    vLeftLayout.addWidget(treeFields)
    #---------LOCKERS----------------------------------------------
    contextText = QLabel("Spogliatoi:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignLeft)
    contextText.setFixedHeight(24)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 15pt;""")
    vLeftLayout.addWidget(contextText)

    # TREE WIDGET LOCKER----------------
    treeLocks = QTreeWidget()
    treeLocks.setHeaderLabels(
        ["Nome", "id", "Genere","Capacità","Aggiunto da", "Data aggiunto"])
    for lock in locker_list:
        item = QTreeWidgetItem([
            str(lock.name),
            str(lock.id),
            str(lock.gender.value),
            str(lock.capacity),
            str(lock.added_by),
            str(lock.data_created.date())
        ])
        treeLocks.addTopLevelItem(item)
    treeLocks.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    treeLocks.setMaximumWidth(650)
    treeLocks.setMinimumWidth(650)
    vLeftLayout.addWidget(treeLocks)
    #----------------------
    LEFT_PART_WIDGET = QWidget()
    LEFT_PART_WIDGET.setLayout(vLeftLayout)
    hSplitter.addWidget(LEFT_PART_WIDGET)
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
    btn_bar_widget = QWidget()
    btn_bar_widget.setFixedHeight(60)
    #--------------------- Add, Del Fields section-------------------------------------------------------
    add_field_btn = QPushButton("Crea Campo")
    add_field_btn.setStyleSheet(style_QButton_white_16Gotham)
    add_field_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_field_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_field_btn = QPushButton("Elimina Campo")
    del_field_btn.setStyleSheet(style_QButton_disabled_16)
    del_field_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_field_btn.setEnabled(False)
    hLayoutBtn.addWidget(del_field_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    #----------------------------------------------------------------------------
    hLayoutBtn.addStretch(1)
    #--------------------- Add, Del Lockers section-------------------------------------------------------
    # add Lock btn
    add_lock_btn = QPushButton("Crea Spogliatoio")
    add_lock_btn.setStyleSheet(style_QButton_white_16Gotham)
    add_lock_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_lock_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_lock_btn = QPushButton("Elimina Spogliatoio")
    del_lock_btn.setStyleSheet(style_QButton_disabled_16)
    del_lock_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_lock_btn.setEnabled(False)
    hLayoutBtn.addWidget(del_lock_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    #----------------------------------------------------------------------------
    btn_bar_widget.setLayout(hLayoutBtn)
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
    usr_center_text = QLabel()
    usr_center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
    bottom_bar.addStretch()
    bottom_bar.addWidget(usr_center_text)
    bottom_bar.addStretch()
    # right btn
    back_btn = QPushButton("Indietro")
    back_btn.setStyleSheet(style_QButton_red)
    #back_btn.clicked.connect(self.init_main_ui)
    bottom_bar.addWidget(back_btn)
    main_layout.addLayout(bottom_bar)
    return (main_layout, usr_center_text,stat_btn,dyna_btn, treeFields, treeLocks,
            label_name,label_surname,label_created_when,label_created_by,label_city,
            label_eta,label_time,label_sport,label_avg_n_player,add_field_btn,del_field_btn,
            add_lock_btn, del_lock_btn,back_btn)
