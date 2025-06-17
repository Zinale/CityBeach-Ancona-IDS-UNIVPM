import PyQt6.QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from PyQt6.uic.Compiler.qtproxies import QtCore

from Controller.Controller import AppController
from Model.Data import AppData
from PyQt6.QtGui import QFontDatabase, QPixmap

style_input_bar = """
    QLineEdit { background-color: #FFFFFF;color: #444444;border: 1px solid #CCCCCC;border-radius: 6px;border-color: #78b395;padding: 4px 12px;
    }
    QLineEdit:hover { background-color: #DCEFFF; } """
style_QButton_verde = """
            QPushButton {
                background-color: #A8E6CF;color: #444444;  border-style: solid; border-width: 1px;border-radius: 14px;border-color: #78b395; padding: 2px 16px;
            }
            QPushButton:hover { background-color: #81C784; }"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CityBeach Ancona | Login")
        self.model = AppData.load_from_file("data.pkl")
        print("Utenti Salvati")
        print(str(self.model.users))
        for utente in self.model.users: print(str(self.model.users[utente]))
        print("\nCurrent user: " + str(self.model.current_user))
        print("\n Articoli Salvati: \n" + str(self.model.articles))
        self.controller = AppController(self.model)
        self.init_login_ui()

    def init_login_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #EAF6FF;")
        a, b = 500, 300
        self.setMinimumSize(PyQt6.QtCore.QSize(a,b))
        self.setMaximumSize(PyQt6.QtCore.QSize(a,b))
        layout = QHBoxLayout()

        layoutV1 = QVBoxLayout()

        #CITY BEACH
        textCity = QLabel("CityBeach | Ancona")
        textCity.setStyleSheet("font-family: Gotham; color: #444444;font-size: 16pt;")  # azzurrino
        textCity.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        #image | LOGO
        imageLogo = QLabel()
        pixmap = QPixmap("src/img/1-1example.png")
        resized_pixmap = pixmap.scaled(180, 180)  # larghezza, altezza
        imageLogo.setPixmap(resized_pixmap)
        imageLogo.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        layoutV1.addWidget(imageLogo)
        layoutV1.addWidget(textCity)

        layoutV1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(layoutV1)

        layoutV2 = QVBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(style_QButton_verde)
        register_btn = QPushButton("Registrati")
        register_btn.setStyleSheet(style_QButton_verde)

        self.user_input.setStyleSheet(style_input_bar)
        self.pass_input.setStyleSheet(style_input_bar)

        login_btn.clicked.connect(self.login)
        register_btn.clicked.connect(self.register)

        # Imposta anche altezza dei widget (fissa)
        self.user_input.setFixedHeight(32)
        self.pass_input.setFixedHeight(32)
        login_btn.setFixedHeight(32)
        register_btn.setFixedHeight(32)

        layoutV2.addWidget(self.user_input)
        layoutV2.addWidget(self.pass_input)
        layoutV2.addSpacing(25)
        layoutV2.addWidget(login_btn)
        layoutV2.addWidget(register_btn)
        layoutV2.setAlignment(Qt.AlignmentFlag.AlignTop)
        layoutV2.setContentsMargins(0, 10, 0, 10)
        layoutV2.setSpacing(10)  # questo evita che siano attaccati tra loro
        layoutV2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layout.addSpacing(30)
        layout.addLayout(layoutV2)

        self.setLayout(layout)

    def init_main_ui(self):
        self.clear_layout()
        layout = QVBoxLayout()
        user = self.controller.get_current_user()

        welcome_label = QLabel(f"Ciao, {user.username}!")
        profile_btn = QPushButton("Visualizza Profilo")
        add_btn = QPushButton("Aggiungi Articolo")
        view_btn = QPushButton("Visualizza Articoli")
        logout_btn = QPushButton("Logout")

        profile_btn.clicked.connect(self.show_profile)
        add_btn.clicked.connect(self.add_article)
        view_btn.clicked.connect(self.view_articles)
        logout_btn.clicked.connect(self.logout)

        layout.addWidget(welcome_label)
        layout.addWidget(profile_btn)
        layout.addWidget(add_btn)
        layout.addWidget(view_btn)
        layout.addWidget(logout_btn)

        self.setLayout(layout)

    def login(self):
        if self.controller.login(self.user_input.text(), self.pass_input.text()):
            self.init_main_ui()
        else:
            QMessageBox.warning(self, "Errore", "Credenziali non valide")

    def register(self):
        if self.controller.register(self.user_input.text(), self.pass_input.text()):
            QMessageBox.information(self, "Registrazione", "Registrazione completata. Ora effettua il login.")
        else:
            QMessageBox.warning(self, "Errore", "Username già esistente")

    def logout(self):
        self.controller.logout()
        self.init_login_ui()

    def add_article(self):
        title, ok = QInputDialog.getText(self, "Nuovo Articolo", "Titolo articolo:")
        if ok and title:
            self.controller.add_article(title)
            QMessageBox.information(self, "Successo", "Articolo aggiunto.")

    def view_articles(self):
        self.clear_layout()
        layout = QVBoxLayout()

        list_widget = QListWidget()
        articles = self.controller.get_all_articles()
        id_map = {}
        for art in articles:
            list_widget.addItem(str(art))
            id_map[str(art)] = art.id

        del_btn = QPushButton("Elimina selezionato (se tuo)")
        back_btn = QPushButton("Indietro")

        def delete_selected():
            selected = list_widget.currentItem()
            if selected:
                article_id = id_map[selected.text()]
                if self.controller.delete_article(article_id):
                    QMessageBox.information(self, "Rimosso", "Articolo eliminato.")
                    self.view_articles()
                else:
                    QMessageBox.warning(self, "Errore", "Non puoi eliminare articoli di altri utenti.")

        del_btn.clicked.connect(delete_selected)
        back_btn.clicked.connect(self.init_main_ui)

        layout.addWidget(QLabel("Articoli pubblicati:"))
        layout.addWidget(list_widget)
        layout.addWidget(del_btn)
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def show_profile(self):
        self.clear_layout()
        layout = QVBoxLayout()

        user = self.controller.get_current_user()

        username_text = QLineEdit()
        password_text = QLineEdit()
        ind_btn = QPushButton('Indietro')
        save_btn = QPushButton('Salva Dati')

        username_text.setText(user.username)
        password_text.setText(user.password)

        def salva_modifiche():
            username_modified = username_text.text()
            password_modified = password_text.text()

            if not username_modified or not password_modified:
                QMessageBox.warning(self, "Errore", "Errore nella modifica")

            status = self.controller.modifica_user(username_modified, password_modified)

            if status:
                QMessageBox.information(self, "Ok", "Dati modificati con successo")
            else:
                QMessageBox.warning(self, "Error", "Impossibile modificare i dati")


        ind_btn.clicked.connect(self.init_main_ui)
        save_btn.clicked.connect(salva_modifiche)


        layout.addWidget(QLabel("Dati:"))
        layout.addWidget(username_text)
        layout.addWidget(password_text)
        layout.addWidget(ind_btn)
        layout.addWidget(save_btn)

        self.setLayout(layout)


    def clear_layout(self):
        if self.layout():
            QWidget().setLayout(self.layout())