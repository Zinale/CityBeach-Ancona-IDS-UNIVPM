import PyQt6.QtCore
from PyQt6.QtGui import QFont, QBrush, QColor
from PyQt6.QtWidgets import QWidget

from Controller.PlayersController import AppPlayersController
from Controller.UsersController import AppUsersController
from Controller.AttrrezzaturaSportivaController import AppSportsEquipmentController
from Model.Data import AppData
from PyQt6.QtGui import QFontDatabase, QPixmap, QIcon,QGuiApplication

from paths import image_path
from .Dipendenti_ui import *
from .Login_ui import *
from .Main_ui import *
from .Player_ui import *
from .styles import *
from .AttrezzaturaSportiva_ui import *
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
        self.users_controller = AppUsersController(self.model.users,self.model.users_next_id)
        self.sport_equipment_controller = AppSportsEquipmentController(self.model.equipment,self.model.equipment_next_it)
        self.players_controller = AppPlayersController(self.model.players,self.model.players_next_id)
        if (self.model.users.__len__() == 0):
            #"admin": "admin" is the first user to be created
            success, status = self.users_controller.register("admin","admin","admin",PyQt6.QtCore.QDate(1,1,1).toString("dd/MM/yyyy"),is_admin = True,password="admin")
            if success:
                self.model.users_next_id = self.users_controller.user_id
                self.model.save_to_file("data.pkl")
        self.selected_user = None
        self.selected_player = None
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
            status, current_User = self.users_controller.login(user_input.text(), pass_input.text())
            if status:
                self.model.current_user = current_User
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
        self.selected_player = None
        #self.showMaximized()
        self.setWindowTitle("CityBeach Ancona | Menù")
        self.center_window()
        #Dipendenti
        def view_dipendenti():
            if self.users_controller.get_current_user().is_admin:
                self.init_dipendenti_ui()
            else:
                QMessageBox.warning(self, "Permesso negato", "Non sei amministratore")
        def show_edit_user_ui():
            dlg = edit_user_ui(parent=self,opener_id=self.users_controller.current_user.id)
            if dlg.exec():
                self.init_main_ui()

        main_layout, btn_campi, btn_pren,btn_play,btn_attspo,btn_dip,btn_rist,center_text,profile_btn,log_btn = main_ui_layout()
        if not self.users_controller.get_current_user().is_admin:
           center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)
        btn_dip.clicked.connect(view_dipendenti)
        btn_attspo.clicked.connect(self.init_sport_equipment_ui)
        btn_play.clicked.connect(self.init_players_ui)
        # Testo centrale
        center_text.setText(f"{self.users_controller.get_current_user().username}")
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

        main_layout, center_text, tree, dip_btn, del_dip_btn,back_btn = view_dipendenti_ui_layout(self.users_controller.get_all_users())
        def show_edit_user_ui():
            dlg = edit_user_ui(parent=self,opener_id=self.users_controller.current_user.id,user_to_edit=self.users_controller.get_user_by_username(self.selected_user.text(4)))
            if dlg.exec():
                self.init_dipendenti_ui()
        def del_dipendente():
            if self.selected_user == None:
                return False
            status, err_id = self.users_controller.delete_user(self.selected_user.text(4))
            if status:
                self.model.save_to_file("data.pkl")
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

        def show_add_dipendente_ui():
            dlg = add_Dipendete_ui(self)
            if dlg.exec():
                self.init_dipendenti_ui()
        tree.itemSelectionChanged.connect(tree_on_item_selected)

        tree.itemDoubleClicked.connect(show_edit_user_ui)

        dip_btn.clicked.connect(show_add_dipendente_ui)

        del_dip_btn.clicked.connect(del_dipendente)
        center_text.setText(f"{self.users_controller.get_current_user().username}")
        if not self.users_controller.get_current_user().is_admin:
            center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)

        back_btn.clicked.connect(self.init_main_ui)
        self.setLayout(main_layout)

    def init_sport_equipment_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(10000, 10000)
        self.setWindowTitle("CityBeach Ancona | Attrezzatura Sportiva")
        self.center_window()

        main_layout, back_btn, att_btn, tree, center_text = view_attrezzaturaSportiva_ui_layout(self.sport_equipment_controller.get_all_equipment())

        def show_add_attrezzatura_ui():
            dlg = add_Attrezzatura_ui(self)
            if dlg.exec():
                self.init_sport_equipment_ui()

        att_btn.clicked.connect(show_add_attrezzatura_ui)
        back_btn.clicked.connect(self.init_main_ui)
        self.setLayout(main_layout)


    def init_players_ui(self):
        #@TODO: fix EDIT function (double-click) and search (+filter) function
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.setMinimumSize(1280, 720)
        self.setMaximumSize(10000, 10000)
        self.selected_player = None
        self.selected_player = None
        self.setWindowTitle("CityBeach Ancona | Giocatori")
        self.center_window()

        (main_layout, center_text, tree, label_name, label_surname, label_created_when,label_created_by, label_city,label_eta, label_time,
         label_sport, label_avg_n_player, add_play_btn, del_play_btn, back_btn)= view_players_ui_layout(list(self.players_controller.players.values()))
        labels = (label_name,label_surname,label_created_when,label_created_by,label_city,label_eta,label_time,label_sport,label_avg_n_player)
        for lab in labels:
            lab.setText("")

        def del_player():
            if self.selected_player == None:
                return False
            confirm = self.confirmDeletePlayer()
            if confirm:
                status, err_id = self.players_controller.delete_player(self.selected_player)
                if status:
                    self.model.save_to_file("data.pkl")
                    self.model = AppData.load_from_file("data.pkl")
                    QMessageBox.information(self, "Rimosso", f"Il profilo di {self.selected_player.name} {self.selected_player.surname} è stato rimosso")
                    self.init_players_ui()
                else:
                    if err_id==1:
                        QMessageBox.critical(self, "Errore", "Errore")
                    elif err_id == 2:
                        QMessageBox.warning(self, "Errore", "Si è verificato un problema durante l'operazione.")
        def show_edit_player_ui():
            dlg = info_Player_ui(parent=self,phase=1,player_to_edit = self.selected_player)
            if dlg.exec():
                self.init_players_ui()
        def tree_on_item_selected():
            selected_player = tree.selectedItems()
            if selected_player and selected_player.__len__() == 1:
                self.selected_player = self.players_controller.findByEmail(selected_player[0].text(4)) #find by email
                del_play_btn.setStyleSheet(style_QButton_white_18Gotham)
                del_play_btn.setEnabled(True)
                #UPDATE STATS
                label_name.setText(self.selected_player.name.upper())
                label_surname.setText(self.selected_player.surname.upper())
                label_created_when.setText(f"Registrato il: {self.selected_player.data_created.date()}")
                label_created_by.setText(f"Registrato da: {self.selected_player.added_by}")
                label_city.setText(f"Città: {self.selected_player.residence}")
            else:
                self.selected_player = None
                del_play_btn.setStyleSheet(style_QButton_disabled)
                del_play_btn.setEnabled(False)
                for lab in labels:
                    lab.setText("")

        def show_add_dipendente_ui():
            dlg = info_Player_ui(parent=self,phase=0)
            if dlg.exec():
                self.init_players_ui()

        tree.itemSelectionChanged.connect(tree_on_item_selected)
        tree.itemDoubleClicked.connect(show_edit_player_ui)

        add_play_btn.clicked.connect(show_add_dipendente_ui)

        del_play_btn.clicked.connect(del_player)
        center_text.setText(f"{self.users_controller.get_current_user().username}")
        if not self.users_controller.get_current_user().is_admin:
            center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)
        back_btn.clicked.connect(self.init_main_ui)
        self.setLayout(main_layout)







    def logout(self):
        self.model.save_to_file("data.pkl")
        self.users_controller.logout()
        self.init_login_ui()

#    def add_article(self):
#        title, ok = QInputDialog.getText(self, "Nuovo Articolo", "Titolo articolo:")
#        if ok and title:
#            self.users_controller.add_article(title)
#            QMessageBox.information(self, "Successo", "Articolo aggiunto.")

    def clear_layout(self):
        if self.layout():
            QWidget().setLayout(self.layout())

    def confirmDeletePlayer(self)-> bool | None:
        reply = QMessageBox.question(self,"Elimina Giocatore", f"Sei sicuro di voler eliminare il profilo di {self.selected_player.name} {self.selected_player.surname}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            return True
        elif reply == QMessageBox.StandardButton.No:
            return False
        return None

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Conferma uscita", "Sei sicuro di voler uscire?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.users_controller.logout()
            sys.exit()
        else:
            try:
                event.ignore()
            except:
                pass

    def center_window(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())