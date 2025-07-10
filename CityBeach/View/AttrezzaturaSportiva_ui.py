import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor, QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, \
    QMessageBox, QGridLayout, QTreeWidget, QTreeWidgetItem, QDialog, QComboBox

from View.styles import (
    style_app_Dialogs,
    style_blackText,
    style_text_gotham_b,
    style_QButton_red,
    style_QButton_white_18Gotham,
    style_QButton_enabled,
    style_QButton_disabled,
)
from View.topBar import topBar
from Model import Data
from Model.EquipmentType import EquipmentType
from Model.SportsCategory import SportsCategory

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
    tree.setHeaderLabels(["Nome", "Tipo", "Disponibilità"])
    
    # Funzione per popolare il QTreeWidget
    def populate_tree():
        tree.clear()

        # Dizionario per la visualizzazione delle attrezzature divise in categorie
        attrezzature = {
            SportsCategory.PADEL: [EquipmentType.PADEL_RACKETS, EquipmentType.PADEL_BALLS],
            SportsCategory.BEACH_VOLLEY: [EquipmentType.BEACH_VOLLEYBALLS],
            SportsCategory.BEACH_TENNIS: [EquipmentType.BEACH_TENNIS_RACKETS, EquipmentType.BEACH_TENNIS_BALLS],
        }

        for sport in attrezzature:
            sport_item = QTreeWidgetItem([sport.value.title()])
            tree.addTopLevelItem(sport_item)
            sport_item.setExpanded(True)

            for att in attrezzature[sport]:
                att_item = QTreeWidgetItem(sport_item)
                att_item.setText(0, att.name.replace("_", " ").title())
                att_item.setText(1, att.value.replace("_", " ").title())
                
                # Trova l'attrezzatura nella lista e ottieni la quantità
                for equipment in lista_attrezzatura:
                    if equipment.equipmentType == att and equipment.name == att.name:
                        att_item.setText(2, str(equipment.quantity))
                        break
                else:
                    att_item.setText(2, "0")
    
    vLayout.addWidget(tree)
    tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    populate_tree()

    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)

    # Funzione per aggiornare lo stato del pulsante "Aggiungi Attrezzatura"
    def update_btn():
        selected = tree.selectedItems()
        if selected:    # controlla se c'è un elemento foglia dell'albero selezionato e abilita il pulsante in caso affermativo
            item = selected[0]
            is_leaf = item.childCount() == 0    
            has_parent = item.parent() is not None
            att_btn.setEnabled(is_leaf and has_parent)
            att_btn.setStyleSheet(style_QButton_enabled if is_leaf and has_parent else style_QButton_white_18Gotham)
        else:
            att_btn.setEnabled(False)
            att_btn.setStyleSheet(style_QButton_disabled)


    # Attrezzatura btn
    att_btn = QPushButton("Aggiungi Attrezzatura")
    att_btn.setStyleSheet(style_QButton_disabled)
    att_btn.setEnabled(False)
    tree.itemSelectionChanged.connect(update_btn)
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


class add_Attrezzatura_ui(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Attrezzatura Sportiva")
        self.setFixedSize(300, 280)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Nome
        name_label = QLabel("Nome:")
        name_label.setStyleSheet(style_text_gotham_b)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(style_blackText)

        # Tipo Attrezzatura
        equipmentType_label = QLabel("Tipo Attrezzatura:")
        equipmentType_label.setStyleSheet(style_text_gotham_b)
        self.equipmentType_comboBox = QComboBox()
        for equipmentType in EquipmentType:
            self.equipmentType_comboBox.addItem(equipmentType.value, equipmentType.name)
        # self.equipmentType_comboBox.setStyleSheet(style_blackText)

        # Disponibilità
        quantity_label = QLabel("Quantità:")
        quantity_label.setStyleSheet(style_text_gotham_b)
        self.quantity_input = QLineEdit()
        self.quantity_input.setStyleSheet(style_blackText)
        self.quantity_input.setPlaceholderText("Inserisci un numero")
        self.quantity_input.setValidator(QIntValidator())  # Accetta solo numeri interi

        # Layout per i campi di input
        grid_layout = QGridLayout()
        grid_layout.addWidget(name_label, 0, 0)
        grid_layout.addWidget(self.name_input, 0, 1)
        grid_layout.addWidget(equipmentType_label, 1, 0)
        grid_layout.addWidget(self.equipmentType_comboBox, 1, 1)
        grid_layout.addWidget(quantity_label, 2, 0)
        grid_layout.addWidget(self.quantity_input, 2, 1)

        layout.addLayout(grid_layout)

        # Pulsanti
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Salva")
        save_button.setStyleSheet(style_QButton_white_18Gotham)
        button_layout.addWidget(save_button)
        def submit_data():
            if hasattr(self.parent().sport_equipment_controller, 'add_equipment'):
                name = self.name_input.text().strip()
                equipmentType = self.equipmentType_comboBox.currentData()   # Ottiene il valore selezionato dalla ComboBox
                # print("Equipment Type:", equipmentType)
                quantity = int(self.quantity_input.text().strip())
                
                success, error_code = self.parent().sport_equipment_controller.add_equipment(name, equipmentType, quantity)
                
                if success:
                    self.parent().model.equipment_next_id = self.parent().sport_equipment_controller.equipment_id
                    self.parent().model.save_to_file("data.pkl")
                    QMessageBox.information(self, "Successo", "Attrezzatura aggiunta con successo!")
                    self.accept()
                else:
                    error_messages = {
                        1: "Nome non valido.",
                        2: "Tipo Attrezzatura non valido.",
                        3: "Quantità deve essere maggiore di zero."
                    }
                    QMessageBox.warning(self, "Errore", error_messages.get(error_code, "Errore sconosciuto."))
            else:
                QMessageBox.warning(self, "Errore", "Controller non disponibile.")

        save_button.clicked.connect(submit_data)
        
        cancel_button = QPushButton("Annulla")
        cancel_button.setStyleSheet(style_QButton_red)
        button_layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.close)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        