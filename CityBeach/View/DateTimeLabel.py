import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, QDateTime, Qt


class DateTimeLabel(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        #self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-family: Gotham; color: #444444; font-size: 16pt;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)

        #timer to update every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # ms

        self.update_datetime()

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        formatted = now.toString("dd/MM/yyyy HH:mm:ss")
        self.label.setText(formatted)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = DateTimeLabel()
    widget.show()
    sys.exit(app.exec())
