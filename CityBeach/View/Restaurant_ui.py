from datetime import datetime

from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QGridLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QTreeWidget, QTreeWidgetItem, QSizePolicy, QFormLayout, QLineEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt
from typing import List

from Controller import AppRestaurantController
from Model.Product import *
from Model.Order import *
from View.topBar import topBar
from View.styles import *


def view_restaurant_ui_layout(products_list:List[Product],delete_mode,remove_product, get_prod_by_name, finalize_order):
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

    products_layout = QVBoxLayout(products_widget)
    products_grid = QGridLayout()
    products_layout.addLayout(products_grid)

    search_bar = QLineEdit()
    search_bar.setPlaceholderText("Cerca prodotto...")
    search_bar.setFixedHeight(35)
    search_bar.setStyleSheet(style_input_bar_white)
    products_layout.addStretch(1)
    products_layout.addWidget(search_bar)
    current_order={}

    category_active = None
    last_clicked = None
    filter_combo_box = QComboBox()
    filter_check_box = QCheckBox("Filtra")

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
    
    def add_to_order(prod):
        if prod and prod.quantity > 0:
            if prod.name in current_order:
                if current_order[prod.name]["qty"] < prod.quantity:
                    current_order[prod.name]["qty"] += 1
            else:
                current_order[prod.name] = {"qty": 1, "price":[p.price for p in products_list if p.name==prod.name][0]}
            update_order_table()
        return True

    def complete_order():
        if not current_order:
            return
        data = {}
        for product_name in current_order:
            data[get_prod_by_name(product_name)] = current_order[product_name]["qty"]

        if finalize_order(data):
            clear_order()
            display_products(category_active,last_clicked)
        return

    def display_products(category,clicked):
        nonlocal category_active
        category_active= category
        nonlocal last_clicked
        last_clicked= clicked
        for btn in categoryButtons:
            if btn == clicked:
                btn.setStyleSheet(style_QButton_red_17Gotham)
            else:
                btn.setStyleSheet(style_QButton_white_16Gotham)
        for i in reversed(range(products_grid.count())):
            widget = products_grid.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        def check_if_add_or_delete(prod:Product):
            if delete_mode() :
                if not prod.isAvailable():
                    if remove_product(prod):
                        display_products(category,clicked)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setWindowTitle("Eliminazione prodotto")
                    msg.setWindowIcon(QIcon("src/img/logo.png"))
                    msg.setText("Non puoi eliminare un prodotto che è presente in magazzino (quantità > 0).")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()
            else:
                add_to_order(prod)

        products =[p for p in products_list if p.type.value==category]
        row, col = 0, 0
        for product in products:
            if filter_check_box.isChecked():
                if filter_combo_box.currentIndex() == 0:
                    if not product.isAvailable():
                        continue
                elif filter_combo_box.currentIndex() == 1:
                    if product.isAvailable():
                        continue
            if search_bar.text().strip().lower() not in product.name.lower():
                continue
            btn = QPushButton(f"{product.name}\n{product.quantity}")
            btn.setMinimumSize(120, 80)
            btn.setStyleSheet(style_products_button)
            btn.clicked.connect(lambda ch, p=product: check_if_add_or_delete(p))
            products_grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def clear_order():
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
    history_btn.setMinimumHeight(35)
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
    send_btn.clicked.connect(complete_order)

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

    #-----------------BUTTONS BAR---------------
    hLayoutBtn = QHBoxLayout()
    #add quantity btn
    qty_btn = QPushButton("Modifica Quantità")
    qty_btn.setStyleSheet(style_QButton_white)
    qty_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(qty_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    filter_check_box.setStyleSheet(style_check_box)
    filter_combo_box.addItems(["Disponibili","Non disponibili"])
    filter_combo_box.setCurrentIndex(0)
    filter_combo_box.setStyleSheet(style_app_Dialogs)
    filter_check_box.stateChanged.connect(lambda c: display_products(category_active,last_clicked))
    filter_combo_box.currentIndexChanged.connect(lambda c: display_products(category_active,last_clicked))
    filter_check_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    filter_combo_box.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(filter_check_box)
    hLayoutBtn.addWidget(filter_combo_box)
    search_bar.textChanged.connect(lambda text: display_products(category_active, last_clicked))

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


    return main_layout, back_btn, qty_btn, history_btn, add_prod, del_prod, center_text

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

class edit_qty_product_ui(QDialog):
    def __init__(self, prod_list:List[Product],search_funct,edit_funct):
        super().__init__()
        self.edit_funct = edit_funct
        self.search_funct = search_funct
        self.setWindowTitle("Modifica Quantità Prodotto")
        self.setFixedSize(300, 200)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.prod_list = prod_list
        self.selected_prod:Product|None = None
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        categoryBar = QComboBox()
        categoryBar.addItems([cat.value for cat in ProductType])
        prodBar = QComboBox()
        quantSpin = QSpinBox()
        quantSpin.setRange(0,999)

        line_old_qty = QLineEdit("0")
        line_new_qty = QLineEdit("0")
        line_new_qty.setReadOnly(True)
        line_old_qty.setReadOnly(True)
        def update_prod_list():
            prodBar.clear()
            prodBar.addItems([p.name for p in self.prod_list if p.type.value==categoryBar.currentText()])
            quantSpin.setValue(0)
            update_texts()
        def update_selected_prod():
            self.selected_prod = self.search_funct(prodBar.currentText())
            update_texts()
        def update_texts():
            try:
                line_old_qty.setText(f"{self.selected_prod.quantity}")
                line_new_qty.setText(f"{self.selected_prod.quantity + quantSpin.value()}")
            except Exception:
                line_old_qty.setText("0")
                line_new_qty.setText("0")
        prodBar.currentTextChanged.connect(update_selected_prod)
        categoryBar.currentTextChanged.connect(update_prod_list)
        quantSpin.textChanged.connect(update_texts)
        save_btn = QPushButton("Salva")
        save_btn.setStyleSheet(style_QButton_red)
        back_btn = QPushButton("Indietro")
        back_btn.setStyleSheet(style_QButton_white)
        back_btn.clicked.connect(self.close)
        update_prod_list()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(save_btn)

        # Styling
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        layout.addRow("Categoria:", categoryBar)
        layout.addRow("Prodotto:", prodBar)
        layout.addRow("Quantità attuale: ", line_old_qty)
        layout.addRow("Quantità da aggiungere: ",quantSpin)
        layout.addRow("Nuova Quantità: ", line_new_qty)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        def submit_data():
            try:
                success = self.edit_funct(self.selected_prod,quantSpin.value())
                if success:
                    QMessageBox.information(self, "Successo", "Quantità modificata.")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Errore", "Errore")
            except:
                QMessageBox.critical(self, "Errore", "Controller non valido.")
                self.close()
        save_btn.clicked.connect(submit_data)
        self.setLayout(main_layout)

class OrdersOverviewDialog(QDialog):
    def __init__(self, orders:List[Order],can_delete_orders:bool,delete_order_funct):
        super().__init__()
        self.setWindowTitle("Storico Ordini")
        layout = QVBoxLayout(self)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.setFixedSize(600, 450)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Dettaglio", "Quantità", "Subtotale"])
        self.tree.setColumnWidth(0, 350)
        self.populate_tree(orders)
        layout.addWidget(self.tree)

        button_layout = QHBoxLayout()
        self.delete_button = QPushButton("Elimina Ordine")
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet(style_QButton_disabled_16)
        button_layout.addWidget(self.delete_button)

        close_button = QPushButton("Chiudi")
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet(style_QButton_white_16Gotham)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        self.setStyleSheet(style_app_Dialogs)
        self.can_delete_orders = can_delete_orders

        def update_delete_button_state():
            selected = self.tree.selectedItems()
            if selected:
                self.delete_button.setEnabled(True)
                self.delete_button.setStyleSheet(style_QButton_red_16Gotham)
            else:
                self.delete_button.setEnabled(False)
                self.delete_button.setStyleSheet(style_QButton_disabled_16)
            return
        def delete_order():
            if not can_delete_orders:
                QMessageBox.warning(self, "Errore", "Solo un amministratore può eliminare un ordine salvato in memoria.")
                return False
            selected = self.tree.selectedItems()
            if selected:
                item = selected[0]
                has_parent = item.parent() is None      #true if the topLevel, else False
                if not has_parent:
                    item = item.parent()        #to get TopLevel
                order_number = int(item.text(0).replace("Ordine #",""))
                reply = QMessageBox.question(self,"Reinserimento prodotti",
                    "Vuoi reinserire i prodotti nell'inventario?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No)
                reinsert = (reply == QMessageBox.StandardButton.Yes)
                delete_order_funct(order_number,reinsert)
                self.populate_tree(orders)

            return

        self.tree.itemSelectionChanged.connect(update_delete_button_state)
        self.delete_button.clicked.connect(delete_order)

    def populate_tree(self, orders:List[Order]):
        self.tree.clear()
        for order_data in orders:
            order_item = QTreeWidgetItem(self.tree)
            order_item.setText(0, f"Ordine #{orders.index(order_data)+1}")
            order_item.setText(2, f"€ {order_data.total_price:.2f}")
            order_item.setFont(0, QFont("Arial", 11, QFont.Weight.Bold))
            timestamp = QTreeWidgetItem(order_item)
            timestamp.setText(0,f"Giorno: {order_data.timestamp.date().strftime("%d/%m/%Y")} Ora: {order_data.timestamp.time().strftime("%H:%M:%S")}")
            timestamp.setText(1,"")
            timestamp.setText(2,"")
            for product, qty in order_data.items.items():
                subtotal = qty * product.price
                product_item = QTreeWidgetItem(order_item)
                product_item.setText(0, f"  - {product.name}")
                product_item.setText(1, str(qty))
                product_item.setText(2, f"€ {subtotal:.2f}")
            order_item.setExpanded(True)