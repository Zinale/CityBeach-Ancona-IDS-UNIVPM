import PyQt6.QtCore

from Controller import *
from Model.Data import AppData
from PyQt6.QtGui import QFontDatabase,QGuiApplication
from PyQt6.QtCore import QTimer
from .Restaurant_ui import *
from .Booking_ui import *
from .Employee_ui import *
from .Fields_Locker_ui import *
from .Login_ui import *
from .Main_ui import *
from .Player_ui import *
from .styles import *
from .SportEquipment_ui import *
from .topBar import *
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","src","fonts","GothamBook.ttf"))
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            raise Exception("Errore nel caricamento del font Gotham")
        self.setWindowIcon(QIcon(image_path("logo.png")))
        self.setWindowFlag(Qt.WindowType.Window)

        #CONTROLLERS
        self.model = AppData.load_from_file("data.pkl")
        self.restaurant_controller=AppRestaurantController(self.model.products, self.model.orders)
        self.users_controller = AppUsersController(self.model.users,self.model.users_next_id)
        self.sport_equipment_controller = AppSportsEquipmentController(self.model.equipment)
        self.players_controller = AppPlayersController(self.model.players,self.model.players_next_id)
        self.fields_controller = AppFieldsController(self.model.fields,self.model.fields_next_id)
        self.lockers_controller = AppLockersController(self.model.lockers,self.model.lockers_next_id)
        self.bookings_controller = AppBookingsController(self.model.bookings,self.model.bookings_next_id)
        if (self.model.users.__len__() == 0):
            #"admin": "admin" is the first user to be created
            data = {
                "name": "admin",
                "surname": "admin",
                "username": "admin",
                "birthday": PyQt6.QtCore.QDate(1,1,1).toString("dd/MM/yyyy"),
                "is_admin": True,
                "gender": Gender.OTHER
            }
            success, status = self.users_controller.register(data,password="admin")
            if success:
                self.model.users_next_id = self.users_controller.user_id
                self.model.save_to_file("data.pkl")
            else:
                QMessageBox.critical(self,"ERRORE AVVIO","NESSUN PROFILO UTENTE ESISTENTE")
                self.close()
        self.selected_user:User | None = None
        self.selected_player:Player | None = None
        self.selected_locker:Locker | None = None
        self.selected_field:Field | None = None
        self.selected_booking:Booking | None= None
        self.delete_mode = False


        self.timerToUpdateBookings = QTimer()
        self.timerToUpdateBookings.timeout.connect(self.check_and_update_bookings)
        self.timerToUpdateBookings.start(30000) #30s

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
            status = self.users_controller.login(user_input.text(), pass_input.text())
            if status:
                self.model.current_user = self.users_controller.get_current_user()
                self.init_main_ui()
            else:
                QMessageBox.warning(self, "Errore", "Credenziali non valide")

        layoutMain, user_input, pass_input, login_btn, close_btn = login_ui_layout()
        login_btn.clicked.connect(login)
        close_btn.clicked.connect(self.closeEvent)
        self.setLayout(layoutMain)

        a, b = 300, 150
        self.resize(a,b)
        #self.showMaximized()        #to avoid the bug: fullscreen's icon active while the window isn't
        #self.showNormal()
        if not self.isMaximized():
            self.center_window()

    def init_main_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.selected_user = None
        self.selected_player = None
        self.selected_locker = None
        self.selected_field = None
        self.selected_booking = None
        a, b = 1100, 700
        self.setMinimumSize(a, b)
        if int(self.width()) < a:
            self.resize(a,b)
        self.setWindowTitle("CityBeach Ancona | Menù")
        if not self.isMaximized():
            self.center_window()
        #Dipendenti
        def view_dipendenti():
            if self.users_controller.get_current_user().is_admin:
                self.init_dipendenti_ui()
            else:
                QMessageBox.warning(self, "Permesso negato", "Non sei amministratore")
        def show_edit_user_ui():
            if self.users_controller.get_current_user().id==1:
                return      #doesn't show admin edit page
            dlg = edit_user_ui(user_to_edit=self.users_controller.current_user,controller_user=self.users_controller)
            if dlg.exec():
                self.init_main_ui()
        main_layout, btn_fields_locks, btn_pren,btn_play,btn_attspo,btn_dip,btn_rist,center_text,profile_btn,log_btn = main_ui_layout()
        if not self.users_controller.get_current_user().is_admin:
           center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)
        btn_fields_locks.clicked.connect(self.init_fields_lockers_static_ui)
        btn_pren.clicked.connect(self.init_bookings_ui)
        btn_dip.clicked.connect(view_dipendenti)
        btn_attspo.clicked.connect(self.init_sport_equipment_ui)
        btn_play.clicked.connect(lambda: self.init_players_ui())
        btn_rist.clicked.connect(self.init_restaurant_ui)
        # Testo centrale
        center_text.setText(f"{self.users_controller.get_current_user().username}")
        profile_btn.clicked.connect(show_edit_user_ui)

        log_btn.clicked.connect(self.logout)
        self.setLayout(main_layout)

    def init_dipendenti_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.selected_user = None
        self.setWindowTitle("CityBeach Ancona | Dipendenti")
        if not self.isMaximized():
            self.center_window()

        main_layout, center_text, table, dip_btn, del_dip_btn,back_btn = view_dipendenti_ui_layout(self.users_controller.get_all_users())

        def show_edit_user_ui():
            if not self.selected_user:
                return
            dlg = edit_user_ui(user_to_edit=self.selected_user, controller_user=self.users_controller)
            nonlocal table
            table.clearSelection()
            if dlg.exec():
                try:
                    table = updateTableEmployees(table,list(self.users_controller.users.values()))
                    self.selected_user = None
                    self.model.save_to_file("data.pkl")
                    #self.init_dipendenti_ui()
                except Exception as E:
                    print(e)
        def del_dipendente():
            if self.selected_user is None:
                return False
            status, err_id = self.users_controller.delete_user(self.selected_user)
            if status:
                self.model.save_to_file("data.pkl")
                self.model = AppData.load_from_file("data.pkl")
                QMessageBox.information(self, "Rimosso", "Utente eliminato.")
                self.init_dipendenti_ui()
                return True
            else:
                if err_id==1:
                    QMessageBox.warning(self, "Errore", "Non puoi eliminare il tuo account.")
                elif err_id==2:
                    QMessageBox.critical(self, "Errore", "Errore")
                elif err_id == 3:
                    QMessageBox.warning(self, "Errore", "Si è verificato un problema durante l'operazione.")
                return False

        def table_on_item_selected():
            selected_items = table.selectedItems()
            if selected_items:
                row = selected_items[0].row()
                username_item = table.item(row, 4)  #username
                if username_item:
                    self.selected_user = self.users_controller.get_user_by_username(username_item.text())

        def show_add_dipendente_ui():
            dlg = add_Dipendete_ui(controller=self.users_controller)
            if dlg.exec():
                self.model.users_next_id = self.users_controller.user_id
                self.model.save_to_file("data.pkl")
                self.init_dipendenti_ui()
        table.itemSelectionChanged.connect(table_on_item_selected)

        table.itemDoubleClicked.connect(show_edit_user_ui)

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
        self.setWindowTitle("CityBeach Ancona | Attrezzatura Sportiva")
        if self.isMaximized():
            self.center_window()

        main_layout, back_btn, qty_btn, tree, center_text = view_attrezzaturaSportiva_ui_layout(self.sport_equipment_controller.get_all_equipment())

        def show_modify_quantity_ui():
            if not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore", "Solo un amministratore può modificare le quantità degli strumenti di gioco")
                return False
            dlg = modify_quantity_ui(tree=tree, controller=self.sport_equipment_controller)
            if dlg.exec():
                self.init_sport_equipment_ui()
                return True
            return False
                    

        # att_btn.clicked.connect(show_add_attrezzatura_ui)
        back_btn.clicked.connect(self.init_main_ui)
        qty_btn.clicked.connect(show_modify_quantity_ui)
        self.setLayout(main_layout)

    def init_players_ui(self,player:Player = None):
        try:
            self.clear_layout()
            self.setStyleSheet("background-color: #FFF0E6;")
            self.selected_player = None
            self.selected_user = None
            self.selected_booking = None
            self.setWindowTitle("CityBeach Ancona | Giocatori")
            if not self.isMaximized():
                self.center_window()
            (main_layout, center_text, table, label_name, label_surname, label_eta, label_created_when,label_created_by, label_city,label_bookings,label_book_lastMonth, label_fav_time,
             label_fav_sport, label_avg_n_player, add_play_btn, del_play_btn, back_btn) = view_players_ui_layout(list(self.players_controller.players.values()))
            labels = (label_name,label_surname,label_eta,label_created_when,label_created_by,label_city,label_bookings,label_book_lastMonth,label_fav_time,label_fav_sport,label_avg_n_player)
            for lab in labels:
                lab.setText("")
            def del_player():
                if self.selected_player is None or not self.users_controller.get_current_user().is_admin:
                    QMessageBox.critical(self, "Errore","Solo un amministratore può rimuovere i giocatori")
                    return False
                confirm = self.confirmDeletePlayer()
                if confirm:
                    status, err_id = self.players_controller.delete_player(self.selected_player)
                    if status:
                        self.model.save_to_file("data.pkl")
                        self.model = AppData.load_from_file("data.pkl")
                        QMessageBox.information(self, "Rimosso", f"Il profilo di {self.selected_player.name} {self.selected_player.surname} è stato rimosso")
                        self.init_players_ui()
                        return True
                    else:
                        if err_id==1:
                            QMessageBox.critical(self, "Errore", "Errore")
                        elif err_id == 2:
                            QMessageBox.warning(self, "Errore", "Si è verificato un problema durante l'operazione.")
                return False

            def show_add_player_ui():
                dlg = info_Player_ui(phase=0, playerController=self.players_controller,
                                     currentUser=self.users_controller.current_user)
                if dlg.exec():
                    self.model.players_next_id = self.players_controller.player_id
                    self.model.save_to_file("data.pkl")
                    self.init_players_ui()

            def show_edit_player_ui():
                #phase = 0 -> register
                #phase = 1 -> edit player
                #print(self.selected_player.id)
                dlg = info_Player_ui(phase=1,player_to_edit = self.selected_player,playerController=self.players_controller)
                nonlocal table
                table.clearSelection()
                if dlg.exec():
                    try:
                        self.selected_player=None
                        self.model.save_to_file("data.pkl")
                        table = updateTablePlayers(table, list(self.players_controller.players.values()))
                        #self.init_players_ui()
                    except Exception as e:
                        print(e)

            def table_on_item_selected():
                selected_player = table.selectedItems()
                try:
                    if selected_player and selected_player.__len__() == 1:
                        row = selected_player[0].row()
                        player_item = table.item(row, 4)  # email
                        if not player_item or not player_item.text():
                            self.selected_player = None
                            return
                        self.selected_player = self.players_controller.findByEmail(player_item.text()) #find by email
                        del_play_btn.setStyleSheet(style_QButton_white_17Gotham)
                        del_play_btn.setEnabled(True)
                        #UPDATE STATS
                        label_name.setText(self.selected_player.name.upper())
                        label_surname.setText(self.selected_player.surname.upper())
                        label_eta.setText(f"Età: {self.selected_player.get_age()}")
                        label_created_when.setText(f"Registrato il: {self.selected_player.data_created.date()}")
                        label_created_by.setText(f"Registrato da: {self.selected_player.added_by}")
                        label_city.setText(f"Città: {self.selected_player.residence}")
                        label_bookings.setText(f"Prenotazioni: {len([b for b in self.bookings_controller.bookings.values() if b.player == self.selected_player])}")
                        label_book_lastMonth.setText(f"Pren. questo mese: {len([b for b in self.bookings_controller.bookings.values() if b.player == self.selected_player and b.time.day.month == date.today().month])}")
                        label_fav_sport.setText(f"Sport Preferito: {self.bookings_controller.getFavoriteSport(self.selected_player)}")
                        label_fav_time.setText(f"Orario Preferito: {self.bookings_controller.getFavoriteTime(self.selected_player)}")
                        label_avg_n_player.setText(f"Media pers/pren: {self.bookings_controller.getAvgPersonForBooking(self.selected_player)}")
                    else:
                        self.selected_player = None
                        del_play_btn.setStyleSheet(style_QButton_disabled)
                        del_play_btn.setEnabled(False)
                        for lab in labels:
                            lab.setText("")
                except Exception as e:
                    print(e)

            table.itemDoubleClicked.connect(show_edit_player_ui)

            add_play_btn.clicked.connect(show_add_player_ui)

            del_play_btn.clicked.connect(del_player)
            center_text.setText(f"{self.users_controller.get_current_user().username}")
            if not self.users_controller.get_current_user().is_admin:
                center_text.setStyleSheet(style_text_red_on_white)
            else:
                center_text.setStyleSheet(style_text_white_on_red)
            back_btn.clicked.connect(self.init_main_ui)
            table.itemSelectionChanged.connect(table_on_item_selected)
            try:
                self.setLayout(main_layout)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)


    def init_fields_lockers_static_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.setWindowTitle("CityBeach Ancona | Campi e Spogliatoi")
        if not self.isMaximized():
            self.center_window()
        self.selected_field = None
        self.selected_locker = None

        (main_layout, usr_center_text, stat_btn, dyna_btn, treeFields, treeLocks,
         img_widget, add_field_btn, del_field_btn,
         add_lock_btn, del_lock_btn, back_btn,view_graphs_btn) = view_fields_lockers_static_ui_layout(list(self.fields_controller.fields.values()),list(self.lockers_controller.lockers.values()))

        dyna_btn.clicked.connect(self.init_fields_lockers_dynamic_ui)
        def del_field():
            if self.selected_field is None or not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore","Solo un amministratore può rimuovere i Campi da Gioco")
                return False
            confirm = self.confirmDeleteField()
            if confirm:
                status, err_id = self.fields_controller.delete_field(self.selected_field)
                if status:
                    self.model.save_to_file("data.pkl")
                    self.model = AppData.load_from_file("data.pkl")
                    QMessageBox.information(self, "Rimosso", f"Il Campo da gioco '{self.selected_field.name}' è stato rimosso")
                    self.init_fields_lockers_static_ui()
                else:
                    if err_id==1:
                        QMessageBox.critical(self, "Errore", "Errore")
                    elif err_id == 2:
                        QMessageBox.warning(self, "Errore", "Si è verificato un problema durante l'operazione.")
        def del_lock():
            if self.selected_locker is None or not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore","Solo un amministratore può rimuovere gli spogliatoi")
                return False
            confirm = self.confirmDeleteLocker()
            if confirm:
                status, err_id = self.lockers_controller.delete_locker(self.selected_locker)
                if status:
                    self.model.save_to_file("data.pkl")
                    self.model = AppData.load_from_file("data.pkl")
                    QMessageBox.information(self, "Rimosso", f"Lo spogliatoio '{self.selected_locker.name}' è stato rimosso")
                    self.init_fields_lockers_static_ui()
                else:
                    if err_id==1:
                        QMessageBox.critical(self, "Errore", "Errore")
                    elif err_id == 2:
                        QMessageBox.warning(self, "Errore", "Si è verificato un problema durante l'operazione.")

        def show_add_field_ui():
            if not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore","Solo un amministratore può creare Campi da Gioco")
                return False
            dlg = add_field_ui(fieldController=self.fields_controller,currentUser=self.users_controller.current_user)
            if dlg.exec():
                self.model.fields_next_id = self.fields_controller.field_id
                self.model.save_to_file("data.pkl")
                self.init_fields_lockers_static_ui()
                return True
            return False
        def show_add_locker_ui():
            if not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore","Solo un amministratore può aggiungere Spogliatoi")
                return False
            dlg = info_locker_ui(self.lockers_controller,phase=0,currentUser=self.users_controller.current_user)
            if dlg.exec():
                self.model.lockers_next_id = self.lockers_controller.locker_id
                self.model.save_to_file("data.pkl")
                self.init_fields_lockers_static_ui()
                return True
            return False
        def show_edit_locker_ui():
            dlg = info_locker_ui(lockersController=self.lockers_controller,phase=1,locker_to_edit=self.selected_locker)
            if dlg.exec():
                self.model.save_to_file("data.pkl")
                self.init_fields_lockers_static_ui()

        def item_on_tree_field_selected():
            try:
                selected_field = treeFields.selectedItems()
                if selected_field and selected_field.__len__() == 1:
                    self.selected_field = self.fields_controller.fields[int(selected_field[0].text(1))]
                    del_field_btn.setStyleSheet(style_QButton_white_16Gotham)
                    del_field_btn.setEnabled(True)
                    treeLocks.clearSelection()
                    del_lock_btn.setStyleSheet(style_QButton_disabled_16)
                    del_lock_btn.setEnabled(False)
                    self.selected_locker = None
                    fields_imgs = ("src/img/padel.png","src/img/beach.png")
                    pixmap = QPixmap(fields_imgs[list(FieldType).index(self.selected_field.sport)])
                    scaled_pixmap = pixmap.scaled(370,350, Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
                    img_widget.setPixmap(scaled_pixmap)
                else:
                    self.selected_field = None
                    del_field_btn.setStyleSheet(style_QButton_disabled_16)
                    del_field_btn.setEnabled(False)
                    img_widget.setPixmap(QPixmap(""))
            except Exception as e:
                print(e)

        def item_on_tree_lockers_selected():
            try:
                selected_locker = treeLocks.selectedItems()
                if selected_locker and selected_locker.__len__() == 1:
                    self.selected_locker = self.lockers_controller.lockers[int(selected_locker[0].text(1))]
                    del_lock_btn.setStyleSheet(style_QButton_white_16Gotham)
                    del_lock_btn.setEnabled(True)
                    treeFields.clearSelection()
                    del_field_btn.setStyleSheet(style_QButton_disabled_16)
                    del_field_btn.setEnabled(False)
                    self.selected_field = None
                    pixmap = QPixmap("src/img/lockers.png")
                    scaled_pixmap = pixmap.scaled(370, 350, Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
                    img_widget.setPixmap(scaled_pixmap)
                else:
                    self.selected_locker = None
                    del_lock_btn.setStyleSheet(style_QButton_disabled_16)
                    del_lock_btn.setEnabled(False)
                    img_widget.setPixmap(QPixmap(""))
            except Exception as e:
                print(e)
        def open_stats_window():
            if not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore", "Solo un amministratore può visualizzare le statistiche")
                return False
            self.window_stats = StatsWindow(self.bookings_controller)
            self.window_stats.show()
            return True

        view_graphs_btn.clicked.connect(open_stats_window)
        treeFields.itemSelectionChanged.connect(item_on_tree_field_selected)
        treeFields.itemDoubleClicked.connect(open_stats_window)
        treeLocks.itemSelectionChanged.connect(item_on_tree_lockers_selected)
        add_field_btn.clicked.connect(show_add_field_ui)
        add_lock_btn.clicked.connect(show_add_locker_ui)
        treeLocks.itemDoubleClicked.connect(show_edit_locker_ui)
        del_field_btn.clicked.connect(del_field)
        del_lock_btn.clicked.connect(del_lock)
        usr_center_text.setText(f"{self.users_controller.get_current_user().username}")
        if not self.users_controller.get_current_user().is_admin:
            usr_center_text.setStyleSheet(style_text_red_on_white)
        else:
            usr_center_text.setStyleSheet(style_text_white_on_red)
        back_btn.clicked.connect(self.init_main_ui)
        self.setLayout(main_layout)

    def init_fields_lockers_dynamic_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.setWindowTitle("CityBeach Ancona | Campi e Spogliatoi")
        if not self.isMaximized():
            self.center_window()
        self.selected_field = None
        self.selected_locker = None

        (main_layout, usr_center_text, stat_btn, dyna_btn, treeFields, treeLocks,
         back_btn) = view_fields_lockers_dynamic_ui_layout(field_list=list(self.fields_controller.fields.values()),locker_list=list(self.lockers_controller.lockers.values()),bookingsController=self.bookings_controller)

        stat_btn.clicked.connect(self.init_fields_lockers_static_ui)
        usr_center_text.setText(f"{self.users_controller.get_current_user().username}")
        if not self.users_controller.get_current_user().is_admin:
            usr_center_text.setStyleSheet(style_text_red_on_white)
        else:
            usr_center_text.setStyleSheet(style_text_white_on_red)

        back_btn.clicked.connect(self.init_main_ui)
        self.setLayout(main_layout)

    def init_bookings_ui(self):
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.selected_booking = None
        self.setWindowTitle("CityBeach Ancona | Prenotazioni")
        if not self.isMaximized():
            self.center_window()
        try:
            main_layout, center_text, table, book_btn, del_book_btn,back_btn = view_booking_ui_layout(list(self.bookings_controller.bookings.values()))
            def cancel_booking():
                if self.selected_booking is None:
                    return False
                if self.selected_booking.state == BookingState.REGISTERED:
                    self.selected_booking.state = BookingState.CANCELLED
                elif self.selected_booking.state == BookingState.CANCELLED:
                    self.selected_booking.state = BookingState.REGISTERED

                self.model.save_to_file("data.pkl")
                self.init_bookings_ui()
                return True

            def table_on_item_selected():
                selected_booking = table.selectedItems()
                if selected_booking and selected_booking.__len__() == 1:
                    row = selected_booking[0].row()
                    bk_item = table.item(row,0)
                    if not bk_item:
                        return
                    self.selected_booking = self.bookings_controller.bookings[int(bk_item.text())]
                    if self.selected_booking.state in (BookingState.REGISTERED,BookingState.CANCELLED):
                        del_book_btn.setStyleSheet(style_QButton_white_16Gotham)
                        del_book_btn.setEnabled(True)
                        if self.selected_booking.state == BookingState.CANCELLED:
                            del_book_btn.setText("Attiva Prenotazione")
                        else:
                            del_book_btn.setText("Annulla Prenotazione")
                else:
                    self.selected_booking = None
                    del_book_btn.setStyleSheet(style_QButton_disabled_16)
                    del_book_btn.setEnabled(False)

            def show_add_booking_ui():
                dlg = add_booking_ui(bookingController=self.bookings_controller,fields_list=list(self.fields_controller.fields.values()),
                                     lockers_list=list(self.lockers_controller.lockers.values()),players_list=list(self.players_controller.players.values()),
                                     currentUser=self.users_controller.current_user, se_list=list(self.sport_equipment_controller.equipment.values()))
                if dlg.exec():
                    self.model.bookings_next_id = self.bookings_controller.booking_id
                    self.model.save_to_file("data.pkl")
                    self.init_bookings_ui()

            table.itemSelectionChanged.connect(table_on_item_selected)

            book_btn.clicked.connect(show_add_booking_ui)
            del_book_btn.clicked.connect(cancel_booking)
            center_text.setText(f"{self.users_controller.get_current_user().username}")
            if not self.users_controller.get_current_user().is_admin:
                center_text.setStyleSheet(style_text_red_on_white)
            else:
                center_text.setStyleSheet(style_text_white_on_red)

            back_btn.clicked.connect(self.init_main_ui)

            self.setLayout(main_layout)
        except Exception as e:
            print(e)

    def init_restaurant_ui(self):
        self.delete_mode = False
        self.clear_layout()
        self.setStyleSheet("background-color: #FFF0E6;")
        self.selected_booking = None
        self.setWindowTitle("CityBeach Ancona | Area Ristoro")
        if not self.isMaximized():
            self.center_window()
        def show_add_product_ui():
            if  not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore","Solo un amministratore può aggiungere nuovi prodotti")
                return False
            dlg = add_product_ui(controller=self.restaurant_controller,prod_list=self.restaurant_controller.products)
            if dlg.exec():
                self.model.save_to_file("data.pkl")
                self.init_restaurant_ui()
                return True
            return False
        def change_delete_mode():
            if not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore", "Solo un amministratore può eliminare i prodotti del magazzino")
                return False
            self.delete_mode = not self.delete_mode
            del_prod.setStyleSheet(style_QButton_red_17Gotham if self.delete_mode else style_QButton_white_17Gotham)
            return True
        def show_edit_qty_ui():
            if  not self.users_controller.get_current_user().is_admin:
                QMessageBox.critical(self, "Errore","Solo un amministratore può cambiare la quantità dei prodotti")
                return False
            dlg = edit_qty_product_ui(self.restaurant_controller.products,self.restaurant_controller.get_product_by_name,self.restaurant_controller.edit_product)
            if dlg.exec():
                self.model.save_to_file("data.pkl")
                self.init_restaurant_ui()
                return True
            return False
        def show_history_ui():
            dlg = OrdersOverviewDialog(self.restaurant_controller.orders,self.users_controller.get_current_user().is_admin,self.restaurant_controller.delete_order)
            if dlg.exec():
                self.model.save_to_file("data.pkl")
                self.init_restaurant_ui()
                return True
            return False
        main_layout, back_btn, qty_btn, history_btn, add_prod, del_prod, center_text = view_restaurant_ui_layout(self.restaurant_controller.products,lambda :self.delete_mode,self.restaurant_controller.remove_product, self.restaurant_controller.get_product_by_name, self.restaurant_controller.finalize_order)
        back_btn.clicked.connect(self.init_main_ui)
        add_prod.clicked.connect(show_add_product_ui)
        del_prod.clicked.connect(change_delete_mode)
        qty_btn.clicked.connect(show_edit_qty_ui)
        history_btn.clicked.connect(show_history_ui)
        center_text.setText(f"{self.users_controller.get_current_user().username}")
        if not self.users_controller.get_current_user().is_admin:
            center_text.setStyleSheet(style_text_red_on_white)
        else:
            center_text.setStyleSheet(style_text_white_on_red)

        self.setLayout(main_layout)


    def logout(self):
        self.model.save_to_file("data.pkl")
        self.users_controller.logout()
        self.init_login_ui()

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
    def confirmDeleteField(self)-> bool | None:
        reply = QMessageBox.question(self,"Rimuovi Campo da Gioco", f"Sei sicuro di voler rimuovere il campo da gioco '{self.selected_field.name}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
        if reply == QMessageBox.StandardButton.Yes:
            return True
        elif reply == QMessageBox.StandardButton.No:
            return False
        return None
    def confirmDeleteLocker(self)-> bool | None:
        reply = QMessageBox.question(self,"Rimuovi Spogliatoio", f"Sei sicuro di voler rimuovere lo spogliatoio '{self.selected_locker.name}'?",
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
            QMessageBox.StandardButton.Yes
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

    def check_and_update_bookings(self):
        self.bookings_controller.check_and_update()
        self.model.save_to_file("data.pkl")
        
        