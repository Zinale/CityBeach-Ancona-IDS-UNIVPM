import PyQt6.QtCore
from PyQt6.QtGui import QFont, QBrush, QColor

from Controller.Controller import AppController
from Model.Data import AppData
from PyQt6.QtGui import QFontDatabase, QPixmap, QIcon,QGuiApplication

from paths import image_path
from .Dialogs import *
from .Dipendenti_ui import view_dipendenti_ui_layout
from .Login_ui import login_ui_layout
from .Main_ui import main_ui_layout
from .styles import *
from .topBar import *
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","src","fonts","GothamBook.ttf"))
        #print("Esiste il file:", os.path.exists(font_path))
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            raise Exception("Errore nel caricamento del font Gotham")
        #fontfamilyGotham = QFontDatabase.applicationFontFamilies(font_id)[0]
        #print(f"Font caricato: {fontfamilyGotham}")  # debug utile

        self.setWindowIcon(QIcon(image_path("logo.png")))
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
        self.setWindowTitle("CityBeach Ancona | Dipendenti")
        self.center_window()

        main_layout, center_text, tree, dip_btn, del_dip_btn,back_btn = view_dipendenti_ui_layout(self.controller.get_all_users())

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

        dip_btn.clicked.connect(self.show_add_dipendente_ui)

        del_dip_btn.clicked.connect(del_dipendente)
        center_text.setText(f"{self.controller.get_current_user().username}")
        if not self.controller.get_current_user().is_admin:
            center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)

        back_btn.clicked.connect(self.init_main_ui)
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
        reply = QMessageBox.question(
            self, "Conferma uscita", "Sei sicuro di voler uscire?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.logout()
            sys.exit()
        else:
            event.ignore()

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

