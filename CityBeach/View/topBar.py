from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel

from View.styles import style_text_gotham_b

from .DateTimeLabel import DateTimeLabel as dt

def topBar() -> QHBoxLayout():
    # --- TOP BAR ------------------------------------------------------------------------------------
    top_bar = QHBoxLayout()
    top_bar.setContentsMargins(0, 0, 0, 0)

    textCity = QLabel("CityBeach | Ancona")
    textCity.setStyleSheet(style_text_gotham_b)
    textCity.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
    current_time = dt()
    current_time.label.setStyleSheet(style_text_gotham_b)
    current_time.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    top_bar.addWidget(textCity)
    top_bar.addStretch()
    top_bar.addWidget(current_time)
    return top_bar