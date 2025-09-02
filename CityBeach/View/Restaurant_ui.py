from datetime import datetime

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QGridLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QTreeWidget, QTreeWidgetItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from typing import List
from Model.Product import *
from View.topBar import topBar
from View.styles import *


def view_restaurant_ui_layout(products_list:List[Product]):
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
                btn.setStyleSheet(style_QButton_red_16Gotham)
            else:
                btn.setStyleSheet(style_QButton_white_16Gotham)
        for i in reversed(range(products_grid.count())):
            widget = products_grid.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        products =[p.name  for p in products_list if p.type.value==category]
        row, col = 0, 0
        for product in products:
            btn = QPushButton(product)
            btn.setMinimumSize(120, 80)
            btn.clicked.connect(lambda ch, p=product: add_to_order(p))
            products_grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

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
   # clear_btn.clicked.connect(self.clear_order)
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


    return main_layout, back_btn, history_btn
    
    

    