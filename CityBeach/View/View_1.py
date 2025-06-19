import PyQt6.QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from PyQt6.uic.Compiler.qtproxies import QtCore

from Controller.Controller import AppController
from Model.Data import AppData
from PyQt6.QtGui import QFontDatabase, QPixmap, QIcon

style_input_bar = """
    QLineEdit {
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #CCCCCC;
        border-radius: 6px;
        padding: 4px 12px;
    }
    QLineEdit:hover {
        background-color: #EEEEEE;
    }
"""
style_QButton_principale = """
    QPushButton {
        background-color: #E30613;
        color: #FFFFFF;
        border: 1px solid #B20510;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #B20510;
    }
"""
style_QButton_secondario = """
    QPushButton {
        background-color: #028B95;
        color: #FFFFFF;
        border: 1px solid #026E7E;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #026E7E;
    }
"""
style_blackText = """
    QLabel, QFrame {
        color: #000000;
    }
"""

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CityBeach Ancona | Login")
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.model = AppData.load_from_file("data.pkl")
        self.controller = AppController(self.model)
        if (self.model.users.__len__() == 0):
            #"admin": "admin" is the first user to be created
            self.controller.register("","",is_admin = True)

        #DEBUG
        print(self.model.users)
        print("\nCurrent user: " + str(self.model.current_user))
        print("\n Articoli Salvati: \n" + str(self.model.articles))

        #to get Screen's size
        #screen = QApplication.primaryScreen()
        #screen_geometry = screen.availableGeometry()
        #self.max_width = screen_geometry.width()
        #self.max_height = screen_geometry.height()
        #print("Screen MAX Size: ",self.max_height,self.max_width)

        self.init_login_ui()

    def init_login_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #EAF6FF;")
        self.setStyleSheet(style_blackText)
        layoutMAIN = QVBoxLayout()
        layoutHor = QHBoxLayout()
        layoutV1 = QVBoxLayout()

        #CITY BEACH
        textCity = QLabel("CityBeach | Ancona")
        textCity.setStyleSheet("font-family: Gotham; color: #444444;font-size: 16pt;")
        textCity.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        #image | LOGO
        imageLogo = QLabel()
        pixmap = QPixmap("src/img/logo.png")
        resized_pixmap = pixmap.scaled(180, 180)  # larghezza, altezza
        imageLogo.setPixmap(resized_pixmap)
        imageLogo.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        layoutV1.addWidget(imageLogo)
        layoutV1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layoutHor.addLayout(layoutV1)

        layoutV2 = QVBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(style_QButton_principale)

        self.user_input.setStyleSheet(style_input_bar)
        self.pass_input.setStyleSheet(style_input_bar)

        login_btn.clicked.connect(self.login)

        # Imposta anche altezza dei widget (fissa)
        self.user_input.setFixedHeight(32)
        self.pass_input.setFixedHeight(32)
        login_btn.setFixedHeight(32)

        layoutV2.addWidget(self.user_input)
        layoutV2.addWidget(self.pass_input)
        layoutV2.addSpacing(35)
        layoutV2.addWidget(login_btn)
        layoutV2.setContentsMargins(0, 10, 0, 10)
        layoutV2.setSpacing(10)  # questo evita che siano attaccati tra loro
        layoutV2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layoutHor.addSpacing(30)
        layoutHor.addLayout(layoutV2)

        layoutMAIN.addLayout(layoutHor)
        layoutMAIN.addWidget(textCity)
        layoutV2.setAlignment(Qt.AlignmentFlag.AlignTop)
        layoutV2.setContentsMargins(0, 10, 0, 10)
        self.setLayout(layoutMAIN)

        a, b = 450, 250
        self.setFixedSize(PyQt6.QtCore.QSize(a,b))

class MainWindow:
    def init_main_ui(self):
        self.clear_layout()

        # 🔓 Sblocca completamente la finestra
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        # ✅ Rendi la finestra ridimensionabile tramite SizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        # ✅ Questo ripristina lo stato "normale" e riattiva il pulsante del quadrato
        self.showNormal()

        # ✅ Facoltativo: apri la finestra subito massimizzata
        #self.showMaximized()

        layout = QVBoxLayout()
        user = self.controller.get_current_user()
        self.setWindowTitle("CityBeach Ancona | Menù")

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

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,"Conferma uscita","Sei sicuro di voler uscire?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No  #evidenziato
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.logout()
            event.accept()  # Chiude la finestra
        else:
            event.ignore()  # Annulla la chiusura