import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QBrush, QColor, QIntValidator
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, \
    QMessageBox, QGridLayout, QTreeWidget, QTreeWidgetItem, QDialog, QComboBox, QSpinBox

from View.styles import *
from View.topBar import topBar
from Model import Data
from Model.SportsEquipment import *
from Model.SportsCategory import *
from Controller import AppSportsEquipmentController

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
    tree.setHeaderLabels(["ID", "Nome", "Tipo", "Disponibilità"])
    
    # Funzione per popolare il QTreeWidget
    def populate_tree():
        tree.clear()
 
        for sport in Sports:
            sport_item = QTreeWidgetItem([sport.value.title()])
            tree.addTopLevelItem(sport_item)
            sport_item.setExpanded(True)

            for att in lista_attrezzatura:
                if att.sportCategory == sport:
                    att_item = QTreeWidgetItem(sport_item)
                    att_item.setText(0, str(att.id))
                    att_item.setText(1, att.name.replace("_", " ").title())
                    att_item.setText(2, att.equipmentType.value.replace("_", " ").title())
                    att_item.setText(3, str(att.quantity))
                    sport_item.addChild(att_item)
        
        for i in range(tree.columnCount()):
            tree.resizeColumnToContents(i)
    
    vLayout.addWidget(tree)
    tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    populate_tree()

    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)

    # Funzione per aggiornare lo stato del pulsante "Aggiungi Attrezzatura"
    def update_btn(btn):
        selected = tree.selectedItems()
        if selected:    # controlla se c'è un elemento foglia dell'albero selezionato e abilita il pulsante in caso affermativo
            item = selected[0]
            is_leaf = item.childCount() == 0    
            has_parent = item.parent() is not None
            btn.setEnabled(is_leaf and has_parent)
            btn.setStyleSheet(style_QButton_enabled if is_leaf and has_parent else style_QButton_disabled)
        else:
            btn.setEnabled(False)
            btn.setStyleSheet(style_QButton_disabled)
    
    vLayout.addLayout(hLayoutBtn)
    vLayout.setSpacing(15)
    main_layout.addLayout(vLayout)

    # Modifica quantità btn
    qty_btn = QPushButton("Modifica Quantità")
    qty_btn.setStyleSheet(style_QButton_disabled)
    qty_btn.setEnabled(False)
    tree.itemSelectionChanged.connect(lambda: update_btn(qty_btn))
    qty_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    hLayoutBtn.addWidget(qty_btn, alignment=Qt.AlignmentFlag.AlignRight)


    # --- BOTTOM BAR ------------------------------------------------------------------------------------
    bottom_bar = QHBoxLayout()
    bottom_bar.setContentsMargins(0, 0, 0, 0)
    
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

    center_text = QLabel()
    center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    bottom_bar.addStretch()
    bottom_bar.addWidget(center_text)
    bottom_bar.addStretch()

    back_btn = QPushButton("Indietro")
    back_btn.setStyleSheet(style_QButton_red)
    bottom_bar.addWidget(back_btn)
    main_layout.addLayout(bottom_bar)
    return main_layout, back_btn, qty_btn, tree, center_text

    
class modify_quantity_ui(QDialog):
    def __init__(self, tree=None, controller:AppSportsEquipmentController=None):
        super().__init__()
        self.tree = tree
        self.controller = controller
        self.setWindowTitle("Modifica Quantità Attrezzatura Sportiva")
        self.setFixedSize(300, 200)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Quantità
        quantity_label = QLabel("Quantità:")
        quantity_label.setStyleSheet(style_text_gotham_b)
        self.quantity_input = QSpinBox()
        self.quantity_input.setStyleSheet(style_blackText)
        self.quantity_input.setMinimum(0)    

        layout.addWidget(quantity_label)
        layout.addWidget(self.quantity_input)

        # Pulsanti
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Salva")
        save_button.setStyleSheet(style_QButton_white_17Gotham)
        button_layout.addWidget(save_button)

        def submit_data():
            selected_items = self.tree.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "Errore", "Nessuna attrezzatura selezionata.")
                return

            selected_item = selected_items[0]

            try:
                equipment_id = int(selected_item.text(0))  # Colonna 0: ID
                new_quantity = self.quantity_input.value()

                success = self.controller.modify_quantity(equipment_id, new_quantity)

                if success:
                    selected_item.setText(3, str(self.controller.get_equipment_by_id(equipment_id).quantity))  # Colonna 3: Disponibilità
                    QMessageBox.information(self, "Successo", "Quantità aggiornata con successo.")
                    self.accept()
                else:
                    QMessageBox.warning(self, "Errore", "Impossibile aggiornare la quantità.")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante la modifica: {str(e)}")


        save_button.clicked.connect(submit_data)
        
        cancel_button = QPushButton("Annulla")
        cancel_button.setStyleSheet(style_QButton_red)
        button_layout.addWidget(cancel_button)
        cancel_button.clicked.connect(self.close)

        layout.addLayout(button_layout)

        self.setLayout(layout)