from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QVBoxLayout, QApplication, QPushButton, QHBoxLayout, QLabel, QLineEdit, QSizePolicy, \
    QMessageBox, QGridLayout



def login_ui_layout() -> QVBoxLayout() and QLineEdit() and QLineEdit() and QPushButton() and QPushButton():
    layoutMAIN = QVBoxLayout()
    layoutHor = QHBoxLayout()
    layoutV1 = QVBoxLayout()

    # CITY BEACH
    textCity = QLabel("CityBeach | Ancona")
    textCity.setStyleSheet(style_text_gotham_b)
    textCity.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    # image | LOGO
    imageLogo = QLabel()
    pixmap = QPixmap("src/img/logo.png")
    resized_pixmap = pixmap.scaled(180, 180)  # larghezza, altezza
    imageLogo.setPixmap(resized_pixmap)
    imageLogo.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    layoutV1.addWidget(imageLogo)
    layoutV1.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    layoutHor.addLayout(layoutV1)

    layoutV2 = QVBoxLayout()
    user_input = QLineEdit()
    user_input.setPlaceholderText("Username")
    pass_input = QLineEdit()
    pass_input.setPlaceholderText("Password")
    pass_input.setEchoMode(QLineEdit.EchoMode.Password)

    user_input.setStyleSheet(style_input_bar_white())
    pass_input.setStyleSheet(style_input_bar_white())

    user_input.setFixedHeight(32)
    pass_input.setFixedHeight(32)

    login_btn = QPushButton("Login")
    login_btn.setStyleSheet(style_QButton_red)
    #login_btn.clicked.connect(self.login)
    login_btn.setFixedHeight(32)

    close_btn = QPushButton("Chiudi")
    close_btn.setStyleSheet(style_QButton_white)
    #close_btn.clicked.connect(self.closeEvent)
    close_btn.setFixedHeight(32)

    layoutV2.addWidget(user_input)
    layoutV2.addWidget(pass_input)
    layoutV2.addSpacing(35)
    layoutV2.addWidget(login_btn)
    layoutV2.addWidget(close_btn)
    layoutV2.setContentsMargins(0, 10, 0, 10)
    layoutV2.setSpacing(10)
    layoutV2.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    layoutHor.addSpacing(30)
    layoutHor.addLayout(layoutV2)

    layoutMAIN.addLayout(layoutHor)
    layoutMAIN.addWidget(textCity)
    layoutV2.setAlignment(Qt.AlignmentFlag.AlignTop)
    layoutV2.setContentsMargins(0, 10, 0, 10)
    return layoutMAIN, user_input, pass_input, login_btn, close_btn



if __name__ == "__main__":
    class Utente:
        pass
    from styles import *
    from DateTimeLabel import *
    app = QApplication(sys.argv)
    window = init_login_ui()
    #window.resize(400, 300)
    window.exec()
else:
    from Model import *
    from .styles import *