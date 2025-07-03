from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, \
    QMessageBox, QGridLayout, QTreeWidget, QTreeWidgetItem

import sys
from View.styles import style_img1_bg, style_text_gotham_b, style_QButton_white, style_QButton_red, \
    style_text_red_on_white, style_text_white_on_red, style_QButton_white_18Gotham
from View.topBar import topBar

def view_attrezzaturaSportiva_ui_layout(lista_attrezzatura):
    # Layout verticale principale
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    vLayout = QVBoxLayout()
    # --- TOP BAR ------------------------------------------------------------------------------------
    main_layout.addLayout(topBar())
    # --- Text + QTreeWidget + Add / ------------------------------------------------------------------------------------
    contextText = QLabel("Lista Attrezzatura Sportiva:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignCenter)  
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;""")
    vLayout.addWidget(contextText)

    tree = QTreeWidget()
    tree.setHeaderLabels(
        ["Nome", "Sport", "Disponibilità"])
    for attrezzatura in lista_attrezzatura:
        item = QTreeWidgetItem([
            str(attrezzatura.name),
            str(attrezzatura.sport),
            str(attrezzatura.availability)
        ])
        tree.addTopLevelItem(item)
    for i in range(50):
        item = QTreeWidgetItem([str(i), str(i), str(i)])
        tree.addTopLevelItem(item)
    vLayout.addWidget(tree)
    tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)

    # Attrezzatura btn
    att_btn = QPushButton("Aggiungi Attrezzatura")
    att_btn.setStyleSheet(style_QButton_white_18Gotham)
    att_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    hLayoutBtn.addWidget(att_btn, alignment=Qt.AlignmentFlag.AlignRight)
    
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

    center_text = QLabel()
    center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    bottom_bar.addStretch()
    bottom_bar.addWidget(center_text)
    bottom_bar.addStretch()

    back_btn = QPushButton("Indietro")
    back_btn.setStyleSheet(style_QButton_red)
    bottom_bar.addWidget(back_btn)
    main_layout.addLayout(bottom_bar)
    return main_layout, back_btn, att_btn, tree, center_text