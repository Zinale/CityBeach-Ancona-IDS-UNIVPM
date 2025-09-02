from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QGridLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt
from typing import List
from Model.Product import *

def view_restaurant_ui_layout(products_list:List[Product]):
    #main_widget = QWidget()
    main_layout = QHBoxLayout()
    
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
    print("a")

    
    
    
    def add_to_order(product_name):
        if product_name in current_order:
            current_order[product_name]["qty"] += 1
        else:
            current_order[product_name] = {"qty": 1, "price":[p.price for p in products_list if p.name==product_name][0]}
        update_order_table()
    print("a")

    def display_products(category):
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
    print("a")

    categories_widget = QWidget()
    categories_layout = QVBoxLayout(categories_widget)
    categories_widget.setFixedWidth(200)
    print("a")

    for category in [cat.value for cat in ProductType]:
        btn = QPushButton(category)
        btn.setMinimumHeight(60)
        btn.clicked.connect(lambda ch, c=category: display_products(c))
        categories_layout.addWidget(btn)
    print("a")

    categories_layout.addStretch()
    history_btn = QPushButton("Storico Ordini")
    history_btn.setMinimumHeight(50)
   # history_btn.clicked.connect(show_orders_overview)
    categories_layout.addWidget(history_btn)

    order_widget = QWidget()
    order_layout = QVBoxLayout(order_widget)
    order_widget.setFixedWidth(350)
    
    order_label = QLabel("Ordine Corrente")
    print("a")

    order_table = QTableWidget()
    order_table.setColumnCount(3)
    order_table.setHorizontalHeaderLabels(["Qtà", "Prodotto", "Prezzo"])
    order_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

    total_label = QLabel("TOTALE: € 0.00")
   # total_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
    total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

    action_buttons_layout = QHBoxLayout()
    clear_btn = QPushButton("Svuota")
   # clear_btn.clicked.connect(self.clear_order)
    send_btn = QPushButton("INVIA ORDINE")
    send_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
    #send_btn.clicked.connect(self.finalize_order)
    print("a")

    action_buttons_layout.addWidget(clear_btn)
    action_buttons_layout.addWidget(send_btn)
    
    order_layout.addWidget(order_label)
    order_layout.addWidget(order_table)
    order_layout.addWidget(total_label)
    order_layout.addLayout(action_buttons_layout)

    main_layout.addWidget(categories_widget)
    main_layout.addWidget(products_widget, 1)
    main_layout.addWidget(order_widget)
    print("a")

    

    return main_layout
    
    

    