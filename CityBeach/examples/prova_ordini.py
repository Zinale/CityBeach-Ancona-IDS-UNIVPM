import sys
from datetime import datetime # Importa datetime per il timestamp
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QGridLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Aggiungi questo import
from PyQt6.QtWidgets import QDialog, QTreeWidget, QTreeWidgetItem, QVBoxLayout

class OrdersOverviewDialog(QDialog):
    """
    Una finestra di dialogo per visualizzare lo storico di tutti gli ordini.
    """
    def __init__(self, orders, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Storico Ordini")
        self.setGeometry(200, 200, 700, 500)

        layout = QVBoxLayout(self)

        # Crea l'albero per visualizzare gli ordini
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Dettaglio", "Quantità", "Subtotale"])
        self.tree.setColumnWidth(0, 350) # Imposta la larghezza della prima colonna

        # Popola l'albero con i dati degli ordini
        self.populate_tree(orders)

        layout.addWidget(self.tree)

        # Pulsante di chiusura
        close_button = QPushButton("Chiudi")
        close_button.clicked.connect(self.accept) # self.accept() chiude la finestra di dialogo
        layout.addWidget(close_button)

    def populate_tree(self, orders):
        self.tree.clear()
        for order_data in orders:
            # Crea la riga principale per ogni ordine
            order_item = QTreeWidgetItem(self.tree)
            order_item.setText(0, f"Ordine #{order_data['id']} ({order_data['timestamp']})")
            order_item.setText(2, f"€ {order_data['total']:.2f}")
            order_item.setFont(0, QFont("Arial", 12, QFont.Weight.Bold))

            # Aggiungi i prodotti come figli di questa riga
            for product_name, details in order_data['items'].items():
                qty = details['qty']
                subtotal = qty * details['price']

                product_item = QTreeWidgetItem(order_item)
                product_item.setText(0, f"  - {product_name}") # Indentazione per chiarezza
                product_item.setText(1, str(qty))
                product_item.setText(2, f"€ {subtotal:.2f}")

            # Espandi tutti gli ordini di default per una visione immediata
            order_item.setExpanded(True)

class PosApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Ordini Bar")
        self.setGeometry(100, 100, 1200, 700)

        # Dati di esempio
        self.menu = {
            "☕ Caffetteria": ["Espresso", "Macchiato", "Cappuccino", "Ginseng", "Orzo"],
            "🥐 Cornetti": ["Vuoto", "Crema", "Cioccolato", "Marmellata"],
            "🥤 Bevande": ["Acqua", "Coca-Cola", "Succo Arancia"]
        }
        self.prices = {
            "Espresso": 1.10, "Macchiato": 1.20, "Cappuccino": 1.50, "Ginseng": 1.60, "Orzo": 1.50,
            "Vuoto": 1.20, "Crema": 1.30, "Cioccolato": 1.30, "Marmellata": 1.30,
            "Acqua": 1.00, "Coca-Cola": 2.50, "Succo Arancia": 2.80
        }
        
        # --- NUOVO: Storico per gli ordini completati ---
        self.completed_orders = []
        self.order_counter = 0

        # --- Layout principale orizzontale (invariato) ---
        main_layout = QHBoxLayout()

        # --- Colonna 1: Categorie (invariato) ---
        categories_layout = QVBoxLayout()
        categories_widget = QWidget()
        categories_widget.setLayout(categories_layout)
        categories_widget.setFixedWidth(200)

        for category in self.menu.keys():
            btn = QPushButton(category)
            btn.setMinimumHeight(60)
            btn.setFont(QFont("Arial", 12))
            btn.clicked.connect(lambda ch, c=category: self.display_products(c))
            categories_layout.addWidget(btn)
        
        # --- NUOVO: Pulsante per vedere lo storico ---
        categories_layout.addStretch()
        history_btn = QPushButton(" Storico Ordini")
        history_btn.setMinimumHeight(50)
        history_btn.clicked.connect(self.show_orders_overview)
        categories_layout.addWidget(history_btn)


        # --- Colonna 2: Prodotti (invariato) ---
        self.products_grid = QGridLayout()
        products_widget = QWidget()
        products_widget.setLayout(self.products_grid)

        # --- Colonna 3: Riepilogo Ordine (invariato, con una modifica al pulsante INVIA) ---
        order_layout = QVBoxLayout()
        order_widget = QWidget()
        order_widget.setLayout(order_layout)
        order_widget.setFixedWidth(350)
        
        order_label = QLabel("Ordine Corrente")
        order_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        self.order_table = QTableWidget()
        self.order_table.setColumnCount(3)
        self.order_table.setHorizontalHeaderLabels(["Qtà", "Prodotto", "Prezzo"])
        self.order_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.total_label = QLabel("TOTALE: € 0.00")
        self.total_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        action_buttons_layout = QHBoxLayout()
        clear_btn = QPushButton("Svuota")
        clear_btn.clicked.connect(self.clear_order)
        send_btn = QPushButton("INVIA ORDINE")
        send_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        # --- MODIFICA: Collega il pulsante alla nuova funzione ---
        send_btn.clicked.connect(self.finalize_order)
        
        action_buttons_layout.addWidget(clear_btn)
        action_buttons_layout.addWidget(send_btn)

        order_layout.addWidget(order_label)
        order_layout.addWidget(self.order_table)
        order_layout.addWidget(self.total_label)
        order_layout.addLayout(action_buttons_layout)

        main_layout.addWidget(categories_widget)
        main_layout.addWidget(products_widget, 1)
        main_layout.addWidget(order_widget)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.clear_order() # Inizializza l'ordine vuoto
        self.display_products(list(self.menu.keys())[0])

    def display_products(self, category):
        # ... (funzione invariata) ...
        for i in reversed(range(self.products_grid.count())):
            self.products_grid.itemAt(i).widget().setParent(None)
        products = self.menu[category]
        row, col = 0, 0
        for product in products:
            btn = QPushButton(product)
            btn.setMinimumSize(120, 80)
            btn.setFont(QFont("Arial", 11))
            btn.clicked.connect(lambda ch, p=product: self.add_to_order(p))
            self.products_grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def add_to_order(self, product_name):
        # ... (funzione invariata) ...
        price = self.prices[product_name]
        if product_name in self.current_order:
            self.current_order[product_name]["qty"] += 1
        else:
            self.current_order[product_name] = {"qty": 1, "price": price}
        self.update_order_table()

    def update_order_table(self):
        # ... (funzione invariata) ...
        self.order_table.setRowCount(0)
        total = 0.0
        for product, data in self.current_order.items():
            row_position = self.order_table.rowCount()
            self.order_table.insertRow(row_position)
            qty, price = data["qty"], data["price"]
            subtotal = qty * price
            total += subtotal
            self.order_table.setItem(row_position, 0, QTableWidgetItem(str(qty)))
            self.order_table.setItem(row_position, 1, QTableWidgetItem(product))
            self.order_table.setItem(row_position, 2, QTableWidgetItem(f"€ {subtotal:.2f}"))
        self.current_total = total # Salva il totale per dopo
        self.total_label.setText(f"TOTALE: € {total:.2f}")

    def clear_order(self):
        self.current_order = {}
        self.update_order_table()

    # --- NUOVA FUNZIONE: Finalizza l'ordine corrente e lo salva ---
    def finalize_order(self):
        if not self.current_order:
            return # Non fare nulla se l'ordine è vuoto

        self.order_counter += 1
        
        # Crea un oggetto con i dettagli dell'ordine
        completed_order = {
            "id": self.order_counter,
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "total": self.current_total,
            "items": self.current_order.copy() # Usa una copia
        }
        
        # Aggiungilo allo storico
        self.completed_orders.append(completed_order)
        print(f"Ordine #{self.order_counter} salvato.") # Feedback per il debug
        
        # Pulisci l'ordine corrente per il prossimo cliente
        self.clear_order()
    
    # --- NUOVA FUNZIONE: Mostra la finestra dello storico ---
    def show_orders_overview(self):
        # Crea e mostra la finestra di dialogo, passandogli la lista degli ordini
        dialog = OrdersOverviewDialog(self.completed_orders, self)
        dialog.exec() # .exec() la rende modale (blocca la finestra principale)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PosApp()
    window.show()
    sys.exit(app.exec())