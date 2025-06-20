import PyQt6.QtCore
from PyQt6.QtCore import Qt,QRect
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QBrush, QColor
from PyQt6.uic.Compiler.qtproxies import QtCore

from datetime import date
from Controller.Controller import AppController
from Model.Data import AppData
from PyQt6.QtGui import QFontDatabase, QPixmap, QIcon,QGuiApplication
from . import DateTimeLabel as dt


from .Dialogs import *
from .styles import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.setWindowFlag(Qt.WindowType.Window)
        self.model = AppData.load_from_file("data.pkl")
        self.controller = AppController(self.model)
        if (self.model.users.__len__() == 0):
            #"admin": "admin" is the first user to be created
            self.controller.register("admin","admin",is_admin = True)

        #DEBUG -------------------------------------------------------
        print(self.model.users)
        print("\nCurrent user: " + str(self.model.current_user))
        print("\n Articoli Salvati: \n" + str(self.model.articles))
        #to get Screen's size
        self.max_width, self.max_height = self.getMaxSize();
        print("Screen MAX Size: ",self.max_width,self.max_height)
        #-------------------------------------------------------
        self.init_login_ui()

    def init_login_ui(self):
        self.clear_layout()
        self.setWindowTitle("CityBeach Ancona | Login")
        self.setStyleSheet(style_blackText)
        self.setStyleSheet("background-color: #FFF0E6;")
        a, b = 450, 250
        self.setMinimumSize(a, b)
        self.resize(a,b)
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
        self.setStyleSheet("background-color: #FFF0E6;")
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(10000,10000)
        #self.showMaximized()

        self.setWindowTitle("CityBeach Ancona | Menù")
        self.center_window()

        # Layout verticale principale
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # --- TOP BAR ------------------------------------------------------------------------------------
        main_layout.addLayout(self.topBar())

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

        #imgCampi = QIcon(QPixmap("src/img/Baby.tux.sit-800x800.png"))
        imgPrenotazioni = QIcon(QPixmap("src/img/logo.png"))
        imgGiocatori = QIcon(QPixmap("src/img/1-1.jpg"))
        imgAttSpo = QIcon(QPixmap("src/img/1-1.png"))
        imgDipend = QIcon(QPixmap("src/img/fullhd.jpg"))
        imgRisto = QIcon(QPixmap("src/img/fullhd.jpg"))

        #CAMPI DA GIOCO
        btn_campi = QPushButton()
        btn_campi.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #btn_campi.setIcon(imgCampi)
        #btn_campi.setIconSize(btn_campi.size())
        btn_campi.setStyleSheet(style_img1_bg)
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
        btn_pren.setStyleSheet(style_img1_bg)
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
        btn_dip.clicked.connect(self.view_dipendenti)
        label_dip = QLabel("Dipendenti")
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

        # --- BOTTOM BAR ------------------------------------------------------------------------------------
        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 0, 0, 0)

        # Logo piccolo (24px di altezza)
        #DA FARE PER TUTTE LE IMMAGINI
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
        center_text = QLabel(f"{self.controller.get_current_user().username}")
        center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if not self.controller.get_current_user().is_admin:
            center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)

        bottom_bar.addStretch()
        bottom_bar.addWidget(center_text)
        bottom_bar.addStretch()

        # Pulsante a destra
        log_btn = QPushButton("Logout")
        log_btn.setStyleSheet(style_QButton_red)
        log_btn.clicked.connect(self.logout)
        bottom_bar.addWidget(log_btn)

        main_layout.addLayout(bottom_bar)

    def init_dipendenti_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(10000, 10000)
        # self.showMaximized()

        self.setWindowTitle("CityBeach Ancona | Dipendenti")
        self.center_window()

        # Layout verticale principale
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        vLayout = QVBoxLayout()

        # --- TOP BAR ------------------------------------------------------------------------------------
        main_layout.addLayout(self.topBar())
        # --- Text + QTreeWidget + Add / ------------------------------------------------------------------------------------
        contextText = QLabel("Lista Dipendenti:")
        contextText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;""")
        vLayout.addWidget(contextText)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Nome", "Cognome", "Amministratore","Username","Data di Nascita","Sesso","Creato il","Creato da"])

        for user in self.controller.get_all_users():
            item = QTreeWidgetItem([
                str(user.name),
                str(user.surname),
                str(user.is_admin),
                str(user.username),
                str(user.birthday),
                str(user.sesso),
                str(user.data_created),
                str(user.added_by)
            ])
            if user.is_admin:
                item.setBackground(0,QBrush(QColor("#E30613")))
                item.setBackground(2,QBrush(QColor("#E30613")))
                item.setForeground(0,QBrush(QColor("#ffffff")))
                item.setForeground(2,QBrush(QColor("#ffffff")))
                item.setBackground(3,QBrush(QColor("#E30613")))
                item.setForeground(3,QBrush(QColor("#ffffff")))
            self.tree.addTopLevelItem(item)

        for i in range(50):
            item = QTreeWidgetItem([str(i),str(i),str(i),str(i),str(i),str(i)])
            self.tree.addTopLevelItem(item)

        vLayout.addWidget(self.tree)
        #vLayout.addSpacing(1)

        # add Dipendente btn
        dip_btn = QPushButton("Crea Dipendente")
        dip_btn.setStyleSheet(style_QButton_white_18Gotham)
        dip_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        dip_btn.clicked.connect(self.open_add_dipendente_ui)

        vLayout.addWidget(dip_btn,alignment=Qt.AlignmentFlag.AlignHCenter)
        vLayout.setSpacing(15)
        main_layout.addLayout(vLayout)

        # --- BOTTOM BAR ------------------------------------------------------------------------------------
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

        # mid text
        center_text = QLabel(f"{self.controller.get_current_user().username}")
        center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if not self.controller.get_current_user().is_admin:
            center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)

        bottom_bar.addStretch()
        bottom_bar.addWidget(center_text)
        bottom_bar.addStretch()

        # right btn
        back_btn = QPushButton("Indietro")
        back_btn.setStyleSheet(style_QButton_red)
        back_btn.clicked.connect(self.init_main_ui)
        bottom_bar.addWidget(back_btn)

        main_layout.addLayout(bottom_bar)
        self.setLayout(main_layout)





















    def login(self):
        if self.controller.login(self.user_input.text(), self.pass_input.text()):
            self.init_main_ui()
        else:
            QMessageBox.warning(self, "Errore", "Credenziali non valide")

    def view_dipendenti(self):
        if self.controller.get_current_user().is_admin:
            self.init_dipendenti_ui()
        else:
            QMessageBox.warning(self, "Permesso negato", "Non sei amminisratore")

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
            self,"Conferma uscita","Sei sicuro di voler uscire?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No  #highlighted
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.logout()
            event.accept()  # close the program
        else:
            event.ignore()  # cancel the request

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

    def topBar(self) -> QHBoxLayout():
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
        return top_bar

    def open_add_dipendente_ui(self):
        dlg = add_Dipendete_ui(self)
        if dlg.exec():
            print("AGGIUNTO!!!!")
            print(dlg.data)
        else:
            print("ANNULLATO")






