from datetime import datetime
from multiprocessing.spawn import prepare
from typing import List

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QIcon, QFont, QBrush, QColor, QGuiApplication
from PyQt6.QtWidgets import (QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QSplitter, QWidget, QDialog,
                             QFormLayout, QLineEdit, QComboBox, QMessageBox, QSpinBox, QHeaderView, QDateEdit, QCheckBox
                             )

from Controller import AppLockersController, AppFieldsController, AppBookingsController
from Model.Data import TIME_SLOTS
from Model.SportsCategory import *
from Model.User import User
from View.styles import *
from View.topBar import topBar
from Model.Locker import Locker, LockerType
from Model.Field import Field
from Model.Gender import Gender

def view_fields_lockers_static_ui_layout(field_list: List[Field], locker_list: List[Locker]):
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
    hStaDynBtnWidget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    vLayout.addWidget(hStaDynBtnWidget, stretch=0, alignment=Qt.AlignmentFlag.AlignCenter)

    # ---------------------------------------------------------------------------------------
    hSplitter = QSplitter(Qt.Orientation.Horizontal)

    # Splitter per layout SINISTRA (testo + tree + testo + tree) + Destra
    vLeftLayout = QVBoxLayout()

    #---------------------------------------------------------------------------------------
    contextText = QLabel("Campi da Gioco:")
    contextText.setAlignment(Qt.AlignmentFlag.AlignLeft)
    contextText.setFixedHeight(24)
    contextText.setStyleSheet("""font-family: Gotham; color: #000000;font-size: 15pt;""")
    vLeftLayout.addWidget(contextText)

    # TREE WIDGET FIELD----------------
    treeFields = QTreeWidget()
    treeFields.setHeaderLabels(["Nome", "id", "Sport", "Aggiunto da", "Data aggiunto"])
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
    treeLocks.setHeaderLabels(["Nome", "id", "Genere", "Capacità", "Tipo", "Aggiunto da", "Data aggiunto"])
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

    # Immagine ridimensionabile dentro layout
    img_container = QWidget()
    img_container.setFixedWidth(480)
    img_layout = QVBoxLayout()
    img_layout.setContentsMargins(0, 0, 0, 0)
    img_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    IMG_WIDGET = QLabel()
    pixmap = QPixmap("src/img/field.png")
    scaled_pixmap = pixmap.scaled(370, 350, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    IMG_WIDGET.setPixmap(scaled_pixmap)
    IMG_WIDGET.setAlignment(Qt.AlignmentFlag.AlignCenter)

    img_layout.addWidget(IMG_WIDGET)
    img_container.setLayout(img_layout)

    LEFT_PART_WIDGET = QWidget()
    LEFT_PART_WIDGET.setLayout(vLeftLayout)

    hSplitter.addWidget(LEFT_PART_WIDGET)
    hSplitter.addWidget(img_container)
    hSplitter.setStretchFactor(0, 1)
    hSplitter.setStretchFactor(1, 0)
    hSplitter.handle(1).setEnabled(False)

    vLayout.addWidget(hSplitter, 1)

    #--------------------- Add, Del Buttons -------------------------------------------------------
    hLayoutBtn = QHBoxLayout()
    btn_bar_widget = QWidget()
    btn_bar_widget.setFixedHeight(60)

    add_field_btn = QPushButton("Crea Campo")
    add_field_btn.setStyleSheet(style_QButton_white_16Gotham)
    add_field_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_field_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_field_btn = QPushButton("Elimina Campo")
    del_field_btn.setStyleSheet(style_QButton_disabled_16)
    del_field_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_field_btn.setEnabled(False)
    hLayoutBtn.addWidget(del_field_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    hLayoutBtn.addStretch(1)
    view_graphs_btn = QPushButton("Visualizza Grafici")
    view_graphs_btn.setStyleSheet(style_QButton_red)
    view_graphs_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(view_graphs_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
    hLayoutBtn.addStretch(1)

    add_lock_btn = QPushButton("Crea Spogliatoio")
    add_lock_btn.setStyleSheet(style_QButton_white_16Gotham)
    add_lock_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    hLayoutBtn.addWidget(add_lock_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    del_lock_btn = QPushButton("Elimina Spogliatoio")
    del_lock_btn.setStyleSheet(style_QButton_disabled_16)
    del_lock_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
    del_lock_btn.setEnabled(False)
    hLayoutBtn.addWidget(del_lock_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

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

    back_btn = QPushButton("Indietro")
    back_btn.setStyleSheet(style_QButton_red)
    bottom_bar.addWidget(back_btn)

    main_layout.addLayout(bottom_bar)

    return (main_layout, usr_center_text, stat_btn, dyna_btn, treeFields, treeLocks,
            IMG_WIDGET, add_field_btn, del_field_btn, add_lock_btn, del_lock_btn, back_btn,view_graphs_btn)

def view_fields_lockers_dynamic_ui_layout(field_list: List[Field],locker_list:List[Locker],bookingsController:AppBookingsController):
    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(10, 10, 10, 10)
    main_layout.setSpacing(10)
    vLayout = QVBoxLayout()

    #function to give color by the current status of a LockerRoom
    def get_color_by_status(locker:Locker,value:int):
        perc = value/locker.capacity *100
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
        treeFields.setHeaderLabels(["Nome/Categoria"] + [st.getAllTime() for st in TIME_SLOTS])
        for sport in FieldType:
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
        treeLocks.setHeaderLabels(["Nome/Categoria"] + [st.getAllTime() for st in TIME_SLOTS])
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
        sportBar.addItems([sport.value for sport in FieldType])

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
                "sport": FieldType(sportBar.currentText())
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
        typeBar.currentTextChanged.connect(lambda: (capacityBar.setValue(1),capacityBar.setEnabled(False)) if typeBar.currentText() == LockerType.INDIVIDUAL.value else capacityBar.setEnabled(True))
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
                typeBar.setCurrentIndex([typ for typ in LockerType].index(self.locker_to_edit.type.value))
        except:
            self.close()

        def update_possible_gender():
            genderCheck.clear()
            genders = [g.value for g in Gender]
            if typeBar.currentText() == LockerType.MAIN.value:
                genders.remove(Gender.OTHER.value)
            genderCheck.addItems(genders)

        update_possible_gender()
        typeBar.currentTextChanged.connect(update_possible_gender)
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

class StatsWindow(QWidget):
    def __init__(self,bookingController:AppBookingsController):
        try:
            super().__init__()
            self.setWindowIcon(QIcon(image_path("logo.png")))
            self.setWindowFlag(Qt.WindowType.Dialog)
            self.setWindowTitle("Grafico")
            self.index = 0
            self.plotListNames = ["Grafico Età Media (tutti i campi)",
                                  "Grafico n° Giocatori (tutti i campi)",
                                  "Grafico Ore prenotate (top 5 Campi attivi)",
                                  "Grafico Andamento Guadagni"]

            assert self.index<=len(self.plotListNames)-1
            self.functions = [bookingController.generate_plot_avg_age_all_fields,
                              bookingController.generate_plot_total_genders_all_fields,
                              bookingController.generate_top5_fields,
                              bookingController.generate_earning_trend]
            assert len(self.functions) == len(self.plotListNames)
            hLayoutTitle = QHBoxLayout()
            self.labelTextPlot = QLabel(f"{self.plotListNames[self.index]}")
            self.labelTextPlot.setStyleSheet(style_text_gotham_b)
            hLayoutTitle.addWidget(self.labelTextPlot)
            hLayoutTitle.addStretch(1)
            self.yearSpinBox = QSpinBox()
            self.yearSpinBox.setRange(2000,3000)
            self.yearSpinBox.setValue(int(datetime.today().year))
            self.yearSpinBox.setStyleSheet(style_spinBox)
            self.yearSpinBox.valueChanged.connect(self.update_plot)
            hLayoutTitle.addWidget(self.yearSpinBox)

            layout = QVBoxLayout()
            self.labelPlot = QLabel()
            self.labelPlot.setScaledContents(True)
            self.update_plot()
            layout.addLayout(hLayoutTitle)
            layout.addWidget(self.labelPlot,alignment=Qt.AlignmentFlag.AlignCenter)
            pulsanti_layout = QHBoxLayout()
            self.btn_back = QPushButton("Indietro")
            self.btn_next = QPushButton("Avanti")
            self.btn_next.setStyleSheet(style_QButton_white)
            self.btn_back.setStyleSheet(style_QButton_white)
            self.btn_next.clicked.connect(self.go_next)
            self.btn_back.clicked.connect(self.go_back)
            self.setStyleSheet("background-color: #FFF0E6;")
            pulsanti_layout.addWidget(self.btn_back)
            pulsanti_layout.addWidget(self.btn_next)
            layout.addLayout(pulsanti_layout)
            self.setFixedSize(600,600)
            self.setLayout(layout)
            self.center_window()

        except Exception as e:
            print(f"Eccezione: {e} {e.args}")
            return

    def update_plot(self):
        try:
            self.labelPlot.setPixmap(self.functions[self.index](self.yearSpinBox.value()))
            self.labelTextPlot.setText(self.plotListNames[self.index])
        except Exception as e:
            print(f"Eccezione: {e} {e.args}")
            return

    def go_next(self):
        self.index = (self.index+ 1) % len(self.plotListNames)
        self.update_plot()

    def go_back(self):
        self.index = (self.index - 1) % len(self.plotListNames)
        self.update_plot()


    def center_window(self):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
