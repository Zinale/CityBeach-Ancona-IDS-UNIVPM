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

style_text_gotham_b = """
        font-family: Gotham; color: #444444;font-size: 16pt;"""

#background - image: url(src / img / fullhd.jpg); / *Percorso immagine * /
style_img1_bg = """
            QPushButton {
                border: none;
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

style_img2_bg = """
    QPushButton {
        border: 1px solid #000000;
        border-radius: 14px;
        padding: 6px 20px;
        background-image: url(src/img/logo.png);
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
    }

    QPushButton:hover {
        background-image: url(src/img/logo.png);
        background-color: rgba(0, 0, 0, 0.2); /* semitrasparente */
        background-blend-mode: darken;  /* <-- Qt non supporta, ma aiuta a capire l’intento */
    }
"""

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
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
        self.setWindowTitle("CityBeach Ancona | Login")
        self.setStyleSheet("background-color: #EAF6FF;")
        self.setStyleSheet(style_blackText)
        layoutMAIN = QVBoxLayout()
        layoutHor = QHBoxLayout()
        layoutV1 = QVBoxLayout()

        #CITY BEACH
        textCity = QLabel("CityBeach | Ancona")
        textCity.setStyleSheet(style_text_gotham_b)
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
        self.resize(a,b)
        self.showMaximized()        #to avoid the bug: fullscreen's icon active while the window isn't
        self.showNormal()
        self.center_window()

    def init_main_ui(self):
        self.clear_layout()

        self.setMinimumSize(1280, 720)
        self.setMaximumSize(10000,10000)
        self.showMaximized()

        self.setWindowTitle("CityBeach Ancona | Menù")

        # Layout verticale principale
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- TOP BAR ------------------------------------------------------------------------------------
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)

        textCity = QLabel("CityBeach | Ancona")
        textCity.setStyleSheet(style_text_gotham_b)
        textCity.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        current_time = dt.DateTimeLabel()
        current_time.label.setStyleSheet(style_text_gotham_b)
        current_time.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        top_bar.addWidget(textCity)
        top_bar.addStretch()
        top_bar.addWidget(current_time)

        main_layout.addLayout(top_bar)

        # --- Core: 2 row x 3 button with text ------------------------------------------------------------------------------------
        core_layout = QGridLayout()
        core_layout.setHorizontalSpacing(40)  # column space
        core_layout.setVerticalSpacing(20)    # row space

        vv1 = QVBoxLayout()
        vv2 = QVBoxLayout()
        vv3 = QVBoxLayout()
        vv4 = QVBoxLayout()
        vv5 = QVBoxLayout()
        vv6 = QVBoxLayout()

        imgCampi = QIcon(QPixmap("src/img/Baby.tux.sit-800x800.png"))
        imgPrenotazioni = QIcon(QPixmap("src/img/logo.png"))
        imgGiocatori = QIcon(QPixmap("src/img/1-1.jpg"))
        imgAttSpo = QIcon(QPixmap("src/img/1-1.png"))
        imgDipend = QIcon(QPixmap("src/img/fullhd.jpg"))
        imgRisto = QIcon(QPixmap("src/img/fullhd.jpg"))

        #CAMPI DA GIOCO
        btn_campi = QPushButton()
        btn_campi.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_campi.setStyleSheet(style_img2_bg)
        btn_campi.setIcon(imgCampi)
        btn_campi.setIconSize(btn_campi.size())
        label_campi = QLabel("Campi da Gioco")
        label_campi.setStyleSheet(style_text_gotham_b)
        label_campi.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        vv1.addWidget(btn_campi)
        vv1.addWidget(label_campi)
        vv1.setSpacing(6)
        core_layout.addLayout(vv1,0,0)

        #PRENOTAZIONE
        btn_pren = QPushButton()
        btn_pren.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_pren.setStyleSheet(style_img2_bg)
        btn_pren.setIcon(imgPrenotazioni)
        btn_pren.setIconSize(btn_pren.size())
        label_pren = QLabel("Prenotazioni")
        label_pren.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label_pren.setStyleSheet(style_text_gotham_b)
        vv2.addWidget(btn_pren)
        vv2.addWidget(label_pren)
        vv2.setSpacing(6)
        core_layout.addLayout(vv2,0,1)

        #Profili Giocatori
        btn_gioc = QPushButton()
        btn_gioc.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_gioc.setStyleSheet(style_img1_bg)
        btn_gioc.setIcon(imgGiocatori)
        btn_gioc.setIconSize(btn_gioc.size())
        label_gioc = QLabel("Profili Giocatori")
        label_gioc.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label_gioc.setStyleSheet(style_text_gotham_b)
        vv3.addWidget(btn_gioc)
        vv3.addWidget(label_gioc)
        vv3.setSpacing(6)
        core_layout.addLayout(vv3,0,2)

        #Att. Sportiva
        btn_attspo = QPushButton()
        btn_attspo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_attspo.setStyleSheet(style_img1_bg)
        btn_attspo.setIcon(imgAttSpo)
        btn_attspo.setIconSize(btn_attspo.size())
        label_attspo = QLabel("Attrezzatura Sportiva")
        label_attspo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label_attspo.setStyleSheet(style_text_gotham_b)
        vv4.addWidget(btn_attspo)
        vv4.addWidget(label_attspo)
        vv4.setSpacing(6)
        core_layout.addLayout(vv4,1,0)

        #Dipendenti
        btn_dip = QPushButton()
        btn_dip.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_dip.setStyleSheet(style_img1_bg)
        btn_dip.setIcon(imgDipend)
        btn_dip.setIconSize(btn_dip.size())
        label_dip = QLabel("Attrezzatura Sportiva")
        label_dip.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label_dip.setStyleSheet(style_text_gotham_b)
        vv5.addWidget(btn_dip)
        vv5.addWidget(label_dip)
        vv5.setSpacing(6)
        core_layout.addLayout(vv5,1,1)

        #Area Ristoro
        btn_rist = QPushButton()
        btn_rist.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_rist.setStyleSheet(style_img1_bg)
        btn_rist.setIcon(imgRisto)
        btn_rist.setIconSize(btn_rist.size())
        label_rist = QLabel("Area ristoro")
        label_rist.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        label_rist.setStyleSheet(style_text_gotham_b)
        vv6.addWidget(btn_rist)
        vv6.addWidget(label_rist)
        vv6.setSpacing(6)
        core_layout.addLayout(vv6,1,2)


        # Permette al layout centrale di espandersi
        for col in range(3):
            core_layout.setColumnStretch(col, 1)
        for row in range(2):
            core_layout.setRowStretch(row, 1)

        main_layout.addLayout(core_layout, stretch=1)

        # --- Barra in basso -------------------------------------------------
        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 0, 0, 0)

        # Logo piccolo (24 px di altezza)
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

        # Testo centrale
        center_text = QLabel("Testo centrale")
        center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        bottom_bar.addStretch()
        bottom_bar.addWidget(center_text)
        bottom_bar.addStretch()

        # Pulsante a destra
        action_button = QPushButton("Azione")
        bottom_bar.addWidget(action_button)

        main_layout.addLayout(bottom_bar)























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