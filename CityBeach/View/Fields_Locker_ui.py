from datetime import datetime
from typing import List

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QFont, QBrush, QColor
from PyQt6.QtWidgets import (QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QSplitter, QWidget, QDialog,
                             QFormLayout, QLineEdit, QComboBox, QMessageBox, QSpinBox, QHeaderView, QDateEdit, QCheckBox
                             )

from Controller import AppLockersController, AppFieldsController, AppBookingsController
from Model.Data import TIME_SLOTS
from Model.SportsCategory import SportsCategory
from Model.User import User
from View.styles import *
from View.topBar import topBar
from Model.Locker import Locker, LockerType
from Model.Field import Field
from Model.Gender import Gender

def view_fields_lockers_static_ui_layout(field_list: List[Field],locker_list:List[Locker]):
    # Layout verticale principale
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    vLayout = QVBoxLayout()
    # --- TOP BAR ------------------------------------------------------------------------------------
    top_bar_widget = QWidget()
    top_bar_widget.setFixedHeight(21)
    top_bar_widget.setLayout(topBar())
    main_layout.addWidget(top_bar_widget)
    # --------STATIC vs DYNAMIC ------------------------------------------------------------------
    hStaDynBtnLayout = QHBoxLayout()
    hStaDynBtnLayout.addStretch(1)
    stat_btn = QPushButton("Statica")
    stat_btn.setStyleSheet(style_QButton_red)
    stat_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    stat_btn.setEnabled(False)
    hStaDynBtnLayout.addWidget(stat_btn)
    hStaDynBtnLayout.addSpacing(10)
    dyna_btn = QPushButton("Dinamica")
    dyna_btn.setStyleSheet(style_QButton_white)
    dyna_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    hStaDynBtnLayout.addWidget(dyna_btn)
    hStaDynBtnLayout.addStretch(1)
    hStaDynBtnWidget = QWidget()
    hStaDynBtnWidget.setLayout(hStaDynBtnLayout)
    hStaDynBtnWidget.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Fixed)
    vLayout.addWidget(hStaDynBtnWidget,alignment=Qt.AlignmentFlag.AlignCenter)
    # ---------------------------------------------------------------------------------------
    hSplitter = QSplitter(Qt.Orientation.Horizontal)
    #splitter per layout SINISTRA (testo + tree + testo + tree) + Destra
    vLeftLayout = QVBoxLayout()
    #---------------------------------------------------------------------------------------
    contextText = QLabel("Campi da Gioco:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignLeft)
    contextText.setFixedHeight(24)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 15pt;""")
    vLeftLayout.addWidget(contextText)
    # TREE WIDGET FIELD----------------
    treeFields = QTreeWidget()
    treeFields.setHeaderLabels(
        ["Nome", "id", "Sport", "Aggiunto da","Data aggiunto"])
    for field in field_list:
        item = QTreeWidgetItem([
            str(field.name),
            str(field.id),
            str(field.sport.value),
            str(field.added_by),
            str(field.data_created.date())
        ])
        treeFields.addTopLevelItem(item)
    treeFields.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    treeFields.setMaximumWidth(650)
    treeFields.setMinimumWidth(650)
    vLeftLayout.addWidget(treeFields)
    #---------LOCKERS----------------------------------------------
    contextText = QLabel("Spogliatoi:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignLeft)
    contextText.setFixedHeight(24)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 15pt;""")
    vLeftLayout.addWidget(contextText)

    # TREE WIDGET LOCKER----------------
    treeLocks = QTreeWidget()
    treeLocks.setHeaderLabels(
        ["Nome", "id", "Genere", "Capacità", "Tipo","Aggiunto da", "Data aggiunto"])
    for lock in locker_list:
        item = QTreeWidgetItem([
            str(lock.name),
            str(lock.id),
            str(lock.gender.value),
            str(lock.capacity),
            str(lock.type.value),
            str(lock.added_by.username),
            str(lock.data_created.date())
        ])
        treeLocks.addTopLevelItem(item)
    treeLocks.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
    treeLocks.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    treeLocks.setMaximumWidth(650)
    treeLocks.setMinimumWidth(650)
    vLeftLayout.addWidget(treeLocks)
    # ----------------------
    LEFT_PART_WIDGET = QWidget()
    LEFT_PART_WIDGET.setLayout(vLeftLayout)
    hSplitter.addWidget(LEFT_PART_WIDGET)
    #--------------Player Stats------------------------------
    stats_widget = QWidget()
    stats_layout = QVBoxLayout(stats_widget)
    stats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    stats_layout.setContentsMargins(10, 10, 10, 10)

    label_name = QLabel("Nome")
    label_name.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 20pt;font-weight: bold;""")
    label_surname = QLabel("Cognome")
    label_surname.setStyleSheet("""font-family: Gotham; color: #E30613;font-size: 20pt;font-weight: bold;""")
    # Etichette vuote che verranno aggiornate dinamicamente
    label_created_when = QLabel("Registrato il: -")
    label_created_when.setStyleSheet(style_text_gotham_b)

    label_created_by = QLabel("Registrato da: -")
    label_created_by.setStyleSheet(style_text_gotham_b)

    label_city = QLabel("Città: -")
    label_city.setStyleSheet(style_text_gotham_b)

    label_eta = QLabel("Prenotazioni: -")
    label_eta.setStyleSheet(style_text_gotham_b)

    label_time = QLabel("Orario Pref.: -")
    label_time.setStyleSheet(style_text_gotham_b)

    label_sport = QLabel("Sport Pref.: -")
    label_sport.setStyleSheet(style_text_gotham_b)

    label_avg_n_player = QLabel("Media pers/pren: -")
    label_avg_n_player.setStyleSheet(style_text_gotham_b)

    # Aggiungi al layout
    stats_layout.addWidget(label_name)
    stats_layout.addWidget(label_surname)
    stats_layout.addWidget(label_created_when)
    stats_layout.addWidget(label_created_by)
    stats_layout.addWidget(label_city)
    stats_layout.addWidget(label_eta)
    stats_layout.addWidget(label_time)
    stats_layout.addWidget(label_sport)
    stats_layout.addWidget(label_avg_n_player)
    stats_layout.setSpacing(12)
    stats_layout.addStretch()

    hSplitter.addWidget(stats_widget)
    # -------------------------------------------------------
    hSplitter.setCollapsible(0,False)
    hSplitter.setStretchFactor(0,0)
    hSplitter.setStretchFactor(1,1)
    hSplitter.handle(1).setEnabled(False)
    vLayout.addWidget(hSplitter)

    hLayoutBtn = QHBoxLayout()
    btn_bar_widget = QWidget()
    btn_bar_widget.setFixedHeight(60)
    #--------------------- Add, Del Fields section-------------------------------------------------------
    add_field_btn = QPushButton("Crea Campo")
    add_field_btn.setStyleSheet(style_QButton_white_16Gotham)
    add_field_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_field_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_field_btn = QPushButton("Elimina Campo")
    del_field_btn.setStyleSheet(style_QButton_disabled_16)
    del_field_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_field_btn.setEnabled(False)
    hLayoutBtn.addWidget(del_field_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    #----------------------------------------------------------------------------
    hLayoutBtn.addStretch(1)
    #--------------------- Add, Del Lockers section-------------------------------------------------------
    # add Lock btn
    add_lock_btn = QPushButton("Crea Spogliatoio")
    add_lock_btn.setStyleSheet(style_QButton_white_16Gotham)
    add_lock_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_lock_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_lock_btn = QPushButton("Elimina Spogliatoio")
    del_lock_btn.setStyleSheet(style_QButton_disabled_16)
    del_lock_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_lock_btn.setEnabled(False)
    hLayoutBtn.addWidget(del_lock_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    #----------------------------------------------------------------------------
    btn_bar_widget.setLayout(hLayoutBtn)
    vLayout.addWidget(btn_bar_widget)
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
    usr_center_text = QLabel()
    usr_center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
    bottom_bar.addStretch()
    bottom_bar.addWidget(usr_center_text)
    bottom_bar.addStretch()
    # right btn
    back_btn = QPushButton("Indietro")
    back_btn.setStyleSheet(style_QButton_red)
    #back_btn.clicked.connect(self.init_main_ui)
    bottom_bar.addWidget(back_btn)
    main_layout.addLayout(bottom_bar)
    return (main_layout, usr_center_text,stat_btn,dyna_btn, treeFields, treeLocks,
            label_name,label_surname,label_created_when,label_created_by,label_city,
            label_eta,label_time,label_sport,label_avg_n_player,add_field_btn,del_field_btn,
            add_lock_btn, del_lock_btn,back_btn)

def view_fields_lockers_dynamic_ui_layout(field_list: List[Field],locker_list:List[Locker],bookingsController:AppBookingsController):
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    vLayout = QVBoxLayout()

    #function to give color by the current status of a LockerRoom
    def get_color_by_status(locker:Locker,value:int):
        perc = int(value/locker.capacity) *100
        if perc>= 75:
            return (RED_COLOR_BG,RED_COLOR_FG)
        elif perc >= 35:
            return (YELLOW_COLOR_BG,YELLOW_COLOR_FG)
        else:
            return (GREEN_COLOR_BG,GREEN_COLOR_FG)

    # --- TOP BAR ------------------------------------------------------------------------------------
    top_bar_widget = QWidget()
    top_bar_widget.setFixedHeight(21)
    top_bar_widget.setLayout(topBar())
    main_layout.addWidget(top_bar_widget)
    # --------STATIC vs DYNAMIC ------------------------------------------------------------------
    hStaDynBtnLayout = QHBoxLayout()
    hStaDynBtnLayout.addStretch(1)
    stat_btn = QPushButton("Statica")
    stat_btn.setStyleSheet(style_QButton_white)
    stat_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    hStaDynBtnLayout.addWidget(stat_btn)
    hStaDynBtnLayout.addSpacing(10)
    dyna_btn = QPushButton("Dinamica")
    dyna_btn.setEnabled(False)
    dyna_btn.setStyleSheet(style_QButton_red)
    dyna_btn.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    hStaDynBtnLayout.addWidget(dyna_btn)
    hStaDynBtnLayout.addStretch(1)
    hStaDynBtnWidget = QWidget()
    hStaDynBtnWidget.setLayout(hStaDynBtnLayout)
    hStaDynBtnWidget.setSizePolicy(QSizePolicy.Policy.Maximum,QSizePolicy.Policy.Fixed)
    main_layout.addWidget(hStaDynBtnWidget,alignment=Qt.AlignmentFlag.AlignCenter)
    # ---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    contextText = QLabel("Campi da Gioco:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignLeft)
    contextText.setFixedHeight(24)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 15pt;""")
    vLayout.addWidget(contextText)
    # TREE WIDGET FIELD----------------
    treeFields = QTreeWidget()
    def populateTreeField():
        treeFields.clear()
        treeFields.setHeaderLabels(["Nome"] + [st.getAllTime() for st in TIME_SLOTS])
        for sport in SportsCategory:
            sport_item = QTreeWidgetItem([sport.value.title()])
            treeFields.addTopLevelItem(sport_item)
            sport_item.setExpanded(True)
            for f in field_list:
                try:
                    if f.sport!=sport:
                        continue
                    item = QTreeWidgetItem([str(f.name)] + [(bookingsController.checkAvailabilityFieldAtTimeSLot(field=f,date=datetime.strptime(byDateSelector.date().toString("dd/MM/yyyy"), "%d/%m/%Y").date(),slot=TS.number))[1]for TS in TIME_SLOTS])
                    if colorsActivatedCheckBox.isChecked():
                        for i in range(1,29):
                            if item.text(i) == "Libero":
                                item.setForeground(i,QBrush(QColor(GREEN_COLOR_FG)))
                                item.setBackground(i,QBrush(QColor(GREEN_COLOR_BG)))
                            else:
                                item.setForeground(i,QBrush(QColor(RED_COLOR_FG)))
                                item.setBackground(i,QBrush(QColor(RED_COLOR_BG)))
                    sport_item.addChild(item)
                except Exception as e:
                    print(e)
        treeFields.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        treeFields.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        for col in range(treeFields.columnCount()):
            treeFields.resizeColumnToContents(col)
        return
    def populateTreeLocker():
        treeLocks.clear()
        treeLocks.setHeaderLabels(["Nome"] + [st.getAllTime() for st in TIME_SLOTS])
        for Ltype in LockerType:
            lock_item = QTreeWidgetItem([Ltype.value.title()])
            treeLocks.addTopLevelItem(lock_item)
            lock_item.setExpanded(True)
            for l in locker_list:
                try:
                    if l.type!=Ltype:
                        continue
                    item = QTreeWidgetItem([str(l.name)] + [
                        (bookingsController.checkStatusLockerAtTimeSlot(locker=l,date=datetime.strptime(byDateSelector.date().toString("dd/MM/yyyy"), "%d/%m/%Y").date(),slot=TS.number)) for TS in TIME_SLOTS])
                    if colorsActivatedCheckBox.isChecked():
                        for i in range(1,29):
                            value = int(item.text(i).split('/')[0])
                            item.setForeground(i,QBrush(QColor(get_color_by_status(l,value)[1])))
                            item.setBackground(i,QBrush(QColor(get_color_by_status(l,value)[0])))
                    lock_item.addChild(item)
                except Exception as e:
                    print(e)
        treeLocks.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        treeLocks.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        for col in range(treeLocks.columnCount()):
            treeLocks.resizeColumnToContents(col)
        return
    vLayout.addWidget(treeFields)
    #---------LOCKERS----------------------------------------------
    contextText = QLabel("Spogliatoi:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignLeft)
    contextText.setFixedHeight(24)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 15pt;""")
    vLayout.addWidget(contextText)
    # TREE WIDGET LOCKER----------------
    treeLocks = QTreeWidget()
    vLayout.addWidget(treeLocks)
    #--------------Date Selector ------------------------------
    hDateLayoutWidget = QWidget()
    hDateLayout = QHBoxLayout()
    hDateLayout.setContentsMargins(10,10,10,10)
    label_title = QLabel("Seleziona Data")
    label_title.setStyleSheet(style_text_gotham_b)
    byDateSelector = QDateEdit()
    byDateSelector.setDisplayFormat("dd/MM/yyyy")
    byDateSelector.setCalendarPopup(True)
    byDateSelector.setFixedSize(150,40)
    byDateSelector.setStyleSheet(style_date_selector)
    byDateSelector.dateChanged.connect(populateTreeField)
    byDateSelector.dateChanged.connect(populateTreeLocker)
    colorsActivatedCheckBox = QCheckBox("Colori")
    colorsActivatedCheckBox.setChecked(False)
    colorsActivatedCheckBox.checkStateChanged.connect(populateTreeField)
    colorsActivatedCheckBox.checkStateChanged.connect(populateTreeLocker)
    colorsActivatedCheckBox.setStyleSheet(style_check_box)
    byDateSelector.setDate(QDate.currentDate())
    # Aggiungi al layout
    hDateLayout.addWidget(label_title,alignment=Qt.AlignmentFlag.AlignCenter)
    hDateLayout.addWidget(byDateSelector,alignment=Qt.AlignmentFlag.AlignCenter)
    hDateLayout.addStretch(1)
    hDateLayout.addWidget(colorsActivatedCheckBox)
    hDateLayoutWidget.setLayout(hDateLayout)

    # -------------------------------------------------------
    vLayout.addWidget(hDateLayoutWidget)
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
    usr_center_text = QLabel()
    usr_center_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
    bottom_bar.addStretch()
    bottom_bar.addWidget(usr_center_text)
    bottom_bar.addStretch()
    # right btn
    back_btn = QPushButton("Indietro")
    back_btn.setStyleSheet(style_QButton_red)
    #back_btn.clicked.connect(self.init_main_ui)
    bottom_bar.addWidget(back_btn)
    main_layout.addLayout(bottom_bar)
    return (main_layout, usr_center_text,stat_btn,dyna_btn, treeFields, treeLocks,
            back_btn)

class add_field_ui(QDialog):
    def __init__(self,fieldController:AppFieldsController,currentUser:User):
        super().__init__()
        self.setWindowTitle("Aggiungi Dipendente")
        self.setFixedSize(300, 160)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.fieldController = fieldController
        self.currentUser = currentUser
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        nameBar = QLineEdit()
        sportBar = QComboBox()
        sportBar.addItems([sport.value for sport in SportsCategory])

        save_btn = QPushButton("Salva")
        save_btn.setStyleSheet(style_QButton_red)

        back_btn = QPushButton("Indietro")
        back_btn.setStyleSheet(style_QButton_white)
        back_btn.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(save_btn)

        # Styling
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        layout.addRow("Nome:", nameBar)
        layout.addRow("Sport:", sportBar)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        def submit_data():
            data = {
                "name": nameBar.text(),
                "sport": SportsCategory(sportBar.currentText())
            }
            # call his parent
            try:
                success, err_id = self.fieldController.register_field(data,self.currentUser.username)
                if success:
                    QMessageBox.information(self, "Successo", "Campo da Gioco aggiunto.")
                    self.accept()
                else:
                    # the controller said: "no!"
                    if err_id != -1:
                        error_messages = {
                            1: "Utente in uso non riconosciuto.",
                            2: "Sport non valido.",
                            3: "Nome non valido.",
                            4: "Nome già in uso per un altro campo."
                        }
                        QMessageBox.warning(self, "Errore", error_messages.get(err_id, "Errore sconosciuto."))
                    else:
                        QMessageBox.critical(self, "Errore", "Errore")
            except:
                QMessageBox.critical(self, "Errore", "Controller non valido.")
                self.close()
        save_btn.clicked.connect(submit_data)
        self.setLayout(main_layout)


class info_locker_ui(QDialog):
    def __init__(self,lockersController:AppLockersController,phase:int=0,locker_to_edit:Locker=None,currentUser:User=None):
        #phase = 0 -> to register new LockerRoom
        #phase = 1 -> to edit an existing LockerRoom
        super().__init__()
        self.lockersController = lockersController
        self.phase = phase
        self.currentUser = currentUser
        self.locker_to_edit = locker_to_edit
        if phase==0:
            self.setWindowTitle("Aggiungi Spogliatoio")
        else:
            self.setWindowTitle(f"Modifica Spogliatoio: {locker_to_edit.name}")
        self.setFixedSize(300, 200)
        self.setStyleSheet(style_app_Dialogs)
        self.setWindowIcon(QIcon("src/img/logo.png"))
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        nameBar = QLineEdit()
        genderCheck = QComboBox()
        genderCheck.addItems([gen.value for gen in Gender])
        capacityBar = QSpinBox()
        capacityBar.setMinimum(1)
        typeBar = QComboBox()
        typeBar.addItems([t.value for t in LockerType])

        save_btn = QPushButton("Salva")
        save_btn.setStyleSheet(style_QButton_red)

        back_btn = QPushButton("Indietro")
        back_btn.setStyleSheet(style_QButton_white)
        back_btn.clicked.connect(self.close)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(save_btn)

        # Styling
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        layout.addRow("Nome:", nameBar)
        layout.addRow("Capacità:", capacityBar)
        layout.addRow("Genere:", genderCheck)
        layout.addRow("Tipo: ",typeBar)

        try:
            if self.phase == 1:
                nameBar.setText(f"{self.locker_to_edit.name}")
                genderCheck.setCurrentIndex([gen.value for gen in Gender].index(self.locker_to_edit.gender.value))
                capacityBar.setValue(self.locker_to_edit.capacity)
        except:
            self.close()

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        def submit_data():
            data = {
                "name": nameBar.text(),
                "gender": Gender(genderCheck.currentText()),
                "capacity":capacityBar.value(),
                "type":LockerType(typeBar.currentText())
            }
            # call his parent
            if self.phase==0:
                #REGISTER NEW LOCKER
                try:
                    success, err_id = self.lockersController.register_locker(data,self.currentUser)
                    if success:
                        QMessageBox.information(self, "Successo", "Spogliatoio aggiunto.")
                        self.accept()
                    else:
                        # the controller said: "no!"
                        if err_id == 1:
                            QMessageBox.warning(self, "Errore", "Nome non valido")
                        elif err_id == 2:
                            QMessageBox.warning(self, "Errore", "Nessuno sta utilizzando il programma")
                        if err_id == 3:
                            QMessageBox.warning(self, "Errore", "Nome già usato")
                        elif err_id == -1:
                            QMessageBox.critical(self, "Errore", "Errore")
                except:
                    QMessageBox.critical(self, "Errore", "Controller non valido/ha riscontrato un errore.")
                    self.close()
            elif self.phase==1:
                #EDIT LOCKER
                try:
                    success, err_id = self.lockersController.edit_locker(data,self.locker_to_edit.id)
                    if success:
                        QMessageBox.information(self, "Successo", f"Spogliatoio '{self.locker_to_edit.name} aggiornato.")
                        self.accept()
                    else:
                        # the controller said: "no!"
                        if err_id == 1:
                            QMessageBox.information(self, "Errore", "Errore nome")
                        elif err_id == 2:
                            QMessageBox.information(self, "Errore", "Errore nome già usato")
                        elif err_id == -1:
                            QMessageBox.critical(self, "Errore", "Errore")
                except:
                    self.close()
        save_btn.clicked.connect(submit_data)
        self.setLayout(main_layout)
