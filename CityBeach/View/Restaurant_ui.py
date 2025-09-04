from datetime import datetime

from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QGridLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QTreeWidget, QTreeWidgetItem, QSizePolicy, QFormLayout, QLineEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QMessageBox
)
from PyQt6.QtCore import Qt
from typing import List

from Controller import AppRestaurantController
from Model.Product import *
from View.topBar import topBar
from View.styles import *


def view_restaurant_ui_layout(products_list:List[Product],delete_mode,remove_product):
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    top_bar_widget = QWidget()
    top_bar_widget.setFixedHeight(21)
    top_bar_widget.setLayout(topBar())
    main_layout.addWidget(top_bar_widget)
    #main_widget = QWidget()
    mid_layout = QHBoxLayout()
    products_widget = QWidget()
    products_grid = QGridLayout(products_widget)
    current_order={}

    def update_order_table():
        order_table.setRowCount(0)
        total = 0.0
        for product, data in current_order.items():
            row_pos = order_table.rowCount()
            order_table.insertRow(row_pos)
            qty, price = data["qty"], data["price"]
            subtotal = qty * price
            total += subtotal
            order_table.setItem(row_pos, 0, QTableWidgetItem(str(qty)))
            order_table.setItem(row_pos, 1, QTableWidgetItem(product))
            order_table.setItem(row_pos, 2, QTableWidgetItem(f"€ {subtotal:.2f}"))
        total_label.setText(f"TOTALE: € {total:.2f}")
    
    def add_to_order(product_name):
        if product_name in current_order:
            current_order[product_name]["qty"] += 1
        else:
            current_order[product_name] = {"qty": 1, "price":[p.price for p in products_list if p.name==product_name][0]}
        update_order_table()

    def display_products(category,clicked):
        for btn in categoryButtons:
            if btn == clicked:
                btn.setStyleSheet(style_QButton_red_17Gotham)
            else:
                btn.setStyleSheet(style_QButton_white_16Gotham)
        for i in reversed(range(products_grid.count())):
            widget = products_grid.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        def check_if_add_or_delete(prod):
            if delete_mode():
                if remove_product(prod):
                    display_products(category,clicked)
            else:
                add_to_order(prod)

        products =[p.name  for p in products_list if p.type.value==category]
        row, col = 0, 0
        for product in products:
            btn = QPushButton(product)
            btn.setMinimumSize(120, 80)
            btn.setStyleSheet(style_products_button)
            btn.clicked.connect(lambda ch, p=product: check_if_add_or_delete(p))
            products_grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def clear_order():
        print("cleaning")
        current_order.clear()
        update_order_table()

    categories_widget = QWidget()
    categories_layout = QVBoxLayout(categories_widget)
    categories_widget.setFixedWidth(200)
    categoryButtons = []
    for category in [cat.value for cat in ProductType]:
        btn = QPushButton(category)
        btn.setMinimumHeight(60)
        btn.clicked.connect(lambda ch, c=category,b=btn: display_products(c,b))
        categories_layout.addWidget(btn)
        categoryButtons.append(btn)
    categoryButtons[0].click()

    categories_layout.addStretch()
    history_btn = QPushButton("Storico Ordini")
    history_btn.setMinimumHeight(50)
   # history_btn.clicked.connect(show_orders_overview)
    history_btn.setStyleSheet(style_QButton_white)
    categories_layout.addWidget(history_btn)

    order_widget = QWidget()
    order_layout = QVBoxLayout(order_widget)
    order_widget.setFixedWidth(350)
    
    order_label = QLabel("Ordine Corrente")
    order_label.setStyleSheet(style_text_gotham_b)
    order_table = QTableWidget()
    order_table.setColumnCount(3)
    order_table.setHorizontalHeaderLabels(["Qtà", "Prodotto", "Prezzo"])
    order_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    total_label = QLabel("TOTALE: € 0.00")
    total_label.setStyleSheet(style_text_gotham_b)
    total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

    action_buttons_layout = QHBoxLayout()
    clear_btn = QPushButton("Svuota")
    clear_btn.setStyleSheet(style_QButton_white_16Gotham)
    clear_btn.clicked.connect(lambda ch: clear_order())
    send_btn = QPushButton("Invia Ordine")
    send_btn.setStyleSheet(style_QButton_green_16Gotham)
    #send_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
    #send_btn.clicked.connect(self.finalize_order)

    action_buttons_layout.addWidget(clear_btn)
    action_buttons_layout.addWidget(send_btn)
    
    order_layout.addWidget(order_label)
    order_layout.addWidget(order_table)
    order_layout.addWidget(total_label)
    order_layout.addLayout(action_buttons_layout)

    mid_layout.addWidget(categories_widget)
    mid_layout.addWidget(products_widget, 1)
    mid_layout.addWidget(order_widget)
    main_layout.addLayout(mid_layout)

    btn_bar = QHBoxLayout()

    #-----------------BUTTONS BAR---------------
    hLayoutBtn = QHBoxLayout()
    hLayoutBtn.addStretch(1)
    # add Product btn
    add_prod = QPushButton("Aggiungi Prodotto")
    add_prod.setStyleSheet(style_QButton_white_17Gotham)
    add_prod.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_prod, alignment=Qt.AlignmentFlag.AlignHCenter)
    #del Product btn
    del_prod = QPushButton("Elimina Prodotto")
    del_prod.setStyleSheet(style_QButton_white_17Gotham)
    del_prod.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(del_prod, alignment=Qt.AlignmentFlag.AlignHCenter)

    main_layout.addLayout(hLayoutBtn)
    #------------------BOTTOM BAR-------------------------
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


    return main_layout, back_btn, history_btn, add_prod, del_prod

class add_product_ui(QDialog):
    def __init__(self, controller:AppRestaurantController, prod_list:List[Product]):
        super().__init__()
        self.setWindowTitle("Aggiungi Prodotto")
        self.setFixedSize(300, 200)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        nameBar = QLineEdit()
        categoryBar = QComboBox()
        categoryBar.addItems([cat.value for cat in ProductType])
        quantSpin = QSpinBox()
        quantSpin.setRange(0,150)
        priceSpin = QDoubleSpinBox()
        priceSpin.setPrefix("€ ")
        priceSpin.setDecimals(2)
        priceSpin.setRange(0.00, 499)
        priceSpin.setSingleStep(0.10)

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
        layout.addRow("Categoria:", categoryBar)
        layout.addRow("Quantità: ",quantSpin)
        layout.addRow("Prezzo: ", priceSpin)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        def submit_data():
            data = {
                "name": nameBar.text(),
                "type": ProductType(categoryBar.currentText()),
                "quantity":quantSpin.value(),
                "price": priceSpin.value()
            }
            # call his parent
            try:
                success, err_id = self.controller.register_product(data)
                if success:
                    QMessageBox.information(self, "Successo", "Prodotto aggiunto.")
                    self.accept()
                else:
                    # the controller said: "no!"
                    if err_id != -1:
                        error_messages = {
                            1: "Nome non valido.",
                            2: "Quantità non valida.",
                            3: "Prezzo non valido.",
                        }
                        QMessageBox.warning(self, "Errore", error_messages.get(err_id, "Errore sconosciuto."))
                    else:
                        QMessageBox.critical(self, "Errore", "Errore")
            except:
                QMessageBox.critical(self, "Errore", "Controller non valido.")
                self.close()
        save_btn.clicked.connect(submit_data)
        self.setLayout(main_layout)
    
    

    