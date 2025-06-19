import PyQt6.QtCore
from PyQt6.QtCore import Qt,QRect
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont
from PyQt6.uic.Compiler.qtproxies import QtCore

from datetime import date
from Controller.Controller import AppController
from Model.Data import AppData
from PyQt6.QtGui import QFontDatabase, QPixmap, QIcon,QGuiApplication
from . import DateTimeLabel as dt

style_input_bar_white = """
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
style_input_bar_red = """
    QLineEdit {
        background-color: #E30613;
        color: #FFFFFF;
        border: 1px solid #B20510;
        border-radius: 6px;
        padding: 4px 12px;
    }
    QLineEdit:hover {
        background-color: #B20510;
    }
"""
style_QButton_red = """
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
style_QButton_white = """
    QPushButton {
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #CCCCCC;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #EEEEEE;
    }
"""
style_blackText = """
    QLabel, QFrame {
        color: #000000;
    }
"""

style_img1_bg = """
            QPushButton {
                border: none;
                background-image: url('src/img/fullhd.jpg');  /* Percorso immagine */
                background-repeat: no-repeat;
                background-position: center;
                background-size: contain;  /* Adatta immagine */
                border: 1px solid #B000000;
                border-radius: 14px;
                padding: 6px 20px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 50);  /* Effetto hover */
            }
        """

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CityBeach Ancona | Login")
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.setWindowFlag(Qt.WindowType.Window)
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
        self.max_width, self.max_height = self.getMaxSize();

        print("Screen MAX Size: ",self.max_width,self.max_height)

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

        self.user_input.setStyleSheet(style_input_bar_white)
        self.pass_input.setStyleSheet(style_input_bar_white)

        self.user_input.setFixedHeight(32)
        self.pass_input.setFixedHeight(32)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(style_QButton_red)
        login_btn.clicked.connect(self.login)
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
        #self.setFixedSize(PyQt6.QtCore.QSize(a,b))
        #self.setMaximumSize(PyQt6.QtCore.QSize(a,b))
        #self.setMinimumSize(PyQt6.QtCore.QSize(a,b))
        #self.setFixedSize(a, b)
        self.resize(a,b)
        self.showMaximized()        #to avoid the bug: fullscreen's icon active while the window isn't
        self.showNormal()
        self.center_window()

    def init_main_ui(self):
        self.clear_layout()

        self.setMinimumSize(1280, 720)
        self.setMaximumSize(10000,10000)
        self.showMaximized()

        layoutMAIN = QVBoxLayout()
        layoutH1 = QHBoxLayout()    #"CITY-BEACH | ANCONA + datetime
        layoutV2 = QVBoxLayout()    #core of the window
        layoutV2H1 = QHBoxLayout()   #1st level of the grid  (3 button)
        layoutV2H2 = QHBoxLayout()   #2nd level of the grid  (3 button)
        layoutH3 = QHBoxLayout()    #logo + user.name

        layout_vv1 = QVBoxLayout()  #for every button: image + text
        layout_vv2 = QVBoxLayout()
        layout_vv3 = QVBoxLayout()
        layout_vv4 = QVBoxLayout()
        layout_vv5 = QVBoxLayout()
        layout_vv6 = QVBoxLayout()

        # CITY BEACH
        textCity = QLabel("CityBeach | Ancona")
        textCity.setStyleSheet("font-family: Gotham; color: #444444;font-size: 16pt;")
        #textCity.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        #datetime
        datetime_labeL = dt.DateTimeLabel()
        datetime_labeL = QLabel(f"{datetime.date.today()}")
        datetime_labeL.label.setStyleSheet("font-family: Gotham; color: #444444;font-size: 16pt;")
        #datetime_labeL.label.setAlignment(Qt.AlignmentFlag.AlignRight| Qt.AlignmentFlag.AlignVCenter)

        layoutH1.addWidget(datetime_labeL)
        layoutH1.addWidget(textCity)
        layoutH1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        campi_btn = QPushButton("")
        #campi_btn.setStyleSheet(style_QButton_red)
        campi_btn.setStyleSheet(style_img1_bg)
        textCampi = QLabel("Campi da Gioco")
        textCampi.setStyleSheet("font-family: Gotham; color: #444444;font-size: 14pt;")
        textCampi.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_vv1.addWidget(campi_btn)
        layout_vv1.addWidget(textCampi)
        layoutV2H1.addLayout(layout_vv1)

        pren_btn = QPushButton("")
        #campi_btn.setStyleSheet(style_QButton_red)
        pren_btn.setStyleSheet(style_img1_bg)
        textPreno = QLabel("Prenotazioni")
        textPreno.setStyleSheet("font-family: Gotham; color: #444444;font-size: 14pt;")
        textPreno.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_vv2.addWidget(pren_btn)
        layout_vv2.addWidget(textPreno)
        layoutV2H1.addLayout(layout_vv2)

        gioc_btn = QPushButton("")
        #campi_btn.setStyleSheet(style_QButton_red)
        gioc_btn.setStyleSheet(style_img1_bg)
        textGioc = QLabel("Giocatori")
        textGioc.setStyleSheet("font-family: Gotham; color: #444444;font-size: 14pt;")
        textGioc.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_vv3.addWidget(gioc_btn)
        layout_vv3.addWidget(textGioc)
        layoutV2H1.addLayout(layout_vv3)

        attSpo_btn = QPushButton("")
        # campi_btn.setStyleSheet(style_QButton_red)
        attSpo_btn.setStyleSheet(style_img1_bg)
        textAtt = QLabel("Inventario")
        textAtt.setStyleSheet("font-family: Gotham; color: #444444;font-size: 14pt;")
        textAtt.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_vv4.addWidget(attSpo_btn)
        layout_vv4.addWidget(textAtt)
        layoutV2H2.addLayout(layout_vv4)

        dipe_btn = QPushButton("")
        # campi_btn.setStyleSheet(style_QButton_red)
        dipe_btn.setStyleSheet(style_img1_bg)
        textDipe = QLabel("Dipendenti")
        textDipe.setStyleSheet("font-family: Gotham; color: #444444;font-size: 14pt;")
        textDipe.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_vv5.addWidget(dipe_btn)
        layout_vv5.addWidget(textDipe)
        layoutV2H2.addLayout(layout_vv5)

        rist_btn = QPushButton("")
        # campi_btn.setStyleSheet(style_QButton_red)
        rist_btn.setStyleSheet(style_img1_bg)
        textRist = QLabel("Area Ristoro")
        textRist.setStyleSheet("font-family: Gotham; color: #444444;font-size: 14pt;")
        textRist.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout_vv6.addWidget(rist_btn)
        layout_vv6.addWidget(textRist)
        layoutV2H2.addLayout(layout_vv6)

        layoutV2.addLayout(layoutV2H1)
        layoutV2.addLayout(layoutV2H2)
        layoutV2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        layoutV2.setSpacing(15)










        layoutMAIN.addLayout(layoutH1)
        layoutMAIN.addLayout(layoutV2)
        layoutMAIN.addLayout(layoutH3)
        self.setLayout(layoutMAIN)













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

    def center_window(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()

        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def getMaxSize(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        return screen_geometry.width(),screen_geometry.height()