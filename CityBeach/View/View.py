import sys

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
from .Login_ui import login_ui_layout
from .Main_ui import main_ui_layout
from .styles import *
from .topBar import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.setWindowFlag(Qt.WindowType.Window)
        self.model = AppData.load_from_file("data.pkl")
        self.controller = AppController(self.model)
        if (self.model.users.__len__() == 0):
            #"admin": "admin" is the first user to be created
            self.controller.register("admin","admin","admin",PyQt6.QtCore.QDate(1,1,1).toString("dd/MM/yyyy"),is_admin = True,gender ="M",password="admin")
        self.init_login_ui()

    def init_login_ui(self):
        self.clear_layout()
        self.setWindowTitle("CityBeach Ancona | Login")
        self.setStyleSheet(style_blackText)
        self.setStyleSheet("background-color: #FFF0E6;")
        a, b = 450, 250
        self.setMinimumSize(a, b)
        self.resize(a,b)

        def login():
            if self.controller.login(user_input.text(), pass_input.text()):
                self.init_main_ui()
            else:
                QMessageBox.warning(self, "Errore", "Credenziali non valide")

        layoutMain, user_input, pass_input, login_btn, close_btn = login_ui_layout()
        login_btn.clicked.connect(login)
        close_btn.clicked.connect(self.closeEvent)
        self.setLayout(layoutMain)

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
        self.selected_user = None
        #self.showMaximized()
        self.setWindowTitle("CityBeach Ancona | Menù")
        self.center_window()
        #Dipendenti
        def view_dipendenti():
            if self.controller.get_current_user().is_admin:
                print("HELLO")
                self.init_dipendenti_ui()
            else:
                QMessageBox.warning(self, "Permesso negato", "Non sei amministratore")

        def show_edit_user_ui():
            dlg = edit_user_ui(self)
            if dlg.exec():
                self.init_main_ui()

        main_layout, btn_campi, btn_pren,btn_gioc,btn_attspo,btn_dip,btn_rist,center_text,profile_btn,log_btn = main_ui_layout()
        if not self.controller.get_current_user().is_admin:
           center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)

        btn_dip.clicked.connect(view_dipendenti)
        # Testo centrale
        center_text.setText(f"{self.controller.get_current_user().username}")
        profile_btn.clicked.connect(show_edit_user_ui)

        log_btn.clicked.connect(self.logout)

        self.setLayout(main_layout)


    def init_dipendenti_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(10000, 10000)
        self.selected_user = None
        # self.showMaximized()

        self.setWindowTitle("CityBeach Ancona | Dipendenti")
        self.center_window()

        # Layout verticale principale
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        vLayout = QVBoxLayout()

        # --- TOP BAR ------------------------------------------------------------------------------------
        main_layout.addLayout(topBar())

        print("ciao")
        # --- Text + QTreeWidget + Add / ------------------------------------------------------------------------------------
        contextText = QLabel("Lista Dipendenti:")
        contextText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;""")
        vLayout.addWidget(contextText)

        tree = QTreeWidget()
        tree.setHeaderLabels(["Nome", "Cognome", "id","Amministratore","Username","Data di Nascita","Sesso","Creato il","Creato da"])
        for user in self.controller.get_all_users():
            item = QTreeWidgetItem([
                str(user.name),
                str(user.surname),
                str(user.id),
                str(user.is_admin),
                str(user.username),
                str(user.birthday),
                str(user.gender),
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
            tree.addTopLevelItem(item)
        for i in range(50):
            item = QTreeWidgetItem([str(i),str(i),str(i),str(i),str(i),str(i)])
            tree.addTopLevelItem(item)
        vLayout.addWidget(tree)
        tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        def del_dipendente():
            if self.selected_user == None:
                return False
            status, err_id = self.controller.delete_user(self.selected_user.text(4))
            if status:
                self.model = AppData.load_from_file("data.pkl")
                QMessageBox.information(self, "Rimosso", "Utente eliminato.")
                self.init_dipendenti_ui()
            else:
                if err_id==1:
                    QMessageBox.warning(self, "Errore", "Non puoi eliminare il tuo account.")
                elif err_id==2:
                    QMessageBox.critical(self, "Errore", "Errore")
                elif err_id == 3:
                    QMessageBox.warning(self, "Errore", "Si è verificato un problema durante l'operazione.")

        def tree_on_item_selected():
            selected_user = tree.selectedItems()
            if selected_user and selected_user.__len__() == 1:
                self.selected_user = selected_user[0]  # it is an QTree Object

        tree.itemSelectionChanged.connect(tree_on_item_selected)

        hLayoutBtn = QHBoxLayout()
        hLayoutBtn.addStretch(1)
        # add Dipendente btn
        dip_btn = QPushButton("Crea Dipendente")
        dip_btn.setStyleSheet(style_QButton_white_18Gotham())
        dip_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        dip_btn.clicked.connect(self.show_add_dipendente_ui)
        hLayoutBtn.addWidget(dip_btn,alignment=Qt.AlignmentFlag.AlignHCenter)

        #delete Dipendente btn
        del_dip_btn = QPushButton("Elimina Dipendente")
        del_dip_btn.setStyleSheet(style_QButton_white_18Gotham())
        del_dip_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        del_dip_btn.clicked.connect(del_dipendente)
        hLayoutBtn.addWidget(del_dip_btn,alignment=Qt.AlignmentFlag.AlignHCenter)

        vLayout.addLayout(hLayoutBtn)
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

    def register_user(self, name, surname, username, birthday, is_admin, gender):
        return self.controller.register(name,surname,username,birthday,is_admin,gender)

    def logout(self):
        self.controller.logout()
        self.init_login_ui()

    def add_article(self):
        title, ok = QInputDialog.getText(self, "Nuovo Articolo", "Titolo articolo:")
        if ok and title:
            self.controller.add_article(title)
            QMessageBox.information(self, "Successo", "Articolo aggiunto.")

    def clear_layout(self):
        if self.layout():
            QWidget().setLayout(self.layout())

    def closeEvent(self, event):
        try:
            reply = QMessageBox.question(
                self,"Conferma uscita","Sei sicuro di voler uscire?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No  #highlighted
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.controller.logout()
                event.accept()  # close the program
            else:
                event.ignore()  # cancel the request
        finally:
            sys.exit()

    def center_window(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()

        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def show_add_dipendente_ui(self):
        dlg = add_Dipendete_ui(self)
        if dlg.exec():
            self.init_dipendenti_ui()

