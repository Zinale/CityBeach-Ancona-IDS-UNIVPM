from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, \
    QMessageBox, QGridLayout, QTreeWidget, QTreeWidgetItem

import sys
from View.Dialogs import edit_user_ui
from View.styles import style_img1_bg, style_text_gotham_b, style_QButton_white, style_QButton_red, \
    style_text_red_on_white, style_text_white_on_red, style_QButton_white_18Gotham
from View.topBar import topBar


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

    tree = QTreeWidget()
    tree.setHeaderLabels(
        ["Nome", "Cognome", "id", "Amministratore", "Username", "Data di Nascita", "Sesso", "Creato il", "Creato da"])
    for user in lista_dipendenti:
        item = QTreeWidgetItem([
            str(user.name),
            str(user.surname),
            str(user.id),
            str(user.is_admin),
            str(user.username),
            str(user.birthday),
            str(user.gender.value),
            str(user.data_created),
            str(user.added_by)
        ])
        if user.is_admin:
            item.setBackground(0, QBrush(QColor("#E30613")))
            item.setBackground(2, QBrush(QColor("#E30613")))
            item.setForeground(0, QBrush(QColor("#ffffff")))
            item.setForeground(2, QBrush(QColor("#ffffff")))
            item.setBackground(3, QBrush(QColor("#E30613")))
            item.setForeground(3, QBrush(QColor("#ffffff")))
        tree.addTopLevelItem(item)
    for i in range(50):
        item = QTreeWidgetItem([str(i), str(i), str(i), str(i), str(i), str(i)])
        tree.addTopLevelItem(item)
    vLayout.addWidget(tree)
    tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)
    # add Dipendente btn
    dip_btn = QPushButton("Crea Dipendente")
    dip_btn.setStyleSheet(style_QButton_white_18Gotham)
    dip_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(dip_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_dip_btn = QPushButton("Elimina Dipendente")
    del_dip_btn.setStyleSheet(style_QButton_white_18Gotham)
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
    return main_layout,center_text, tree, dip_btn, del_dip_btn,back_btn