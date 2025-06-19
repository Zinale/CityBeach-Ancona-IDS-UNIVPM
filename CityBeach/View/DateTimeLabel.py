import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, QDateTime

class DateTimeLabel(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel(self)
        #self.label.setStyleSheet("font-size: 20px;")

        # tiemr to update every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)  #ms

        self.update_datetime()

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        formatted = now.toString("dd/MM/yyyy HH:mm:ss")
        self.label.setText(formatted)
