from PyQt6.QtCore import QUrl

from paths import image_path

style_input_bar_white = """
    QLineEdit {
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #CCCCCC;
        border-radius: 14px;
        padding: 4px 12px;
    }
    QLineEdit:hover {
        background-color: #EEEEEE;
    }
"""
style_input_bar_red = """
    QLineEdit {
        background-color: #E30613;
        color: #FFFFFF;
        border: 1px solid #B20510;
        border-radius: 14px;
        padding: 4px 12px;
    }
    QLineEdit:hover {
        background-color: #B20510;
    }
"""
style_QButton_red = """
    QPushButton {
        background-color: #E30613;
        color: #FFFFFF;
        border: 1px solid #B20510;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #B20510;
    }
"""

style_QButton_white = """
    QPushButton {
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #CCCCCC;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #EEEEEE;
    }
"""
style_QButton_white_17Gotham ="""
    QPushButton {
        font-family: Gotham; font-size: 17pt;
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #E30613;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #EEEEEE;
        border: 2px solid #E30613;
    }
"""
style_QButton_green_16Gotham ="""
    QPushButton {
        font-family: Gotham; font-size: 16pt;
        background-color: #4CAF50;
        color: #ffffff;
        border: 2px solid #22b600;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #22b600;
        border: 2px solid #009c1a;
    }
"""
style_QButton_white_16Gotham ="""
    QPushButton {
        font-family: Gotham; font-size: 16pt;
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #E30613;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #EEEEEE;
        border: 2px solid #E30613;
    }
"""
style_QButton_red_17Gotham = """
    QPushButton {
        font-family: Gotham; font-size: 17pt;
        background-color: #E30613;
        color: #ffffff;
        border: 1px solid #E30613;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #B20510;
        border: 2px solid #E30613;
    }
"""
style_QButton_red_16Gotham = """
    QPushButton {
        font-family: Gotham; font-size: 16pt;
        background-color: #E30613;
        color: #ffffff;
        border: 1px solid #E30613;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #B20510;
        border: 2px solid #E30613;
    }
"""
style_QButton_enabled = """
    QPushButton {
        font-family: Gotham; font-size: 18pt;
        background-color: #E53935;
        color: #FFFFFF;                 
        border: 1px solid #B71C1C;      
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #B20510;
    }
"""
style_QButton_disabled = """
    QPushButton {
        font-family: Gotham; font-size: 18pt;
        background-color: #FFFFFF;
        color: #9e9e9e;
        border: 1px solid #CCCCCC;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #EEEEEE;
    }
"""
style_QButton_disabled_16 = """
    QPushButton {
        font-family: Gotham; font-size: 16pt;
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #CCCCCC;
        border-radius: 14px;
        padding: 6px 20px;
    }
    QPushButton:hover {
        background-color: #EEEEEE;
    }
"""
style_blackText = """
    QLabel, QFrame {
        color: #000000;
    }
"""

style_text_gotham_b = """
        font-family: Gotham; color: #444444;font-size: 16pt;"""

style_text_red_on_white="""
        font-family: Gotham; color: #E30613;background-color:#ffffff; font-size: 16pt; border: 2px solid #E30613;
        padding: 6px 20px;
        border-radius: 14px;"""

style_text_white_on_red = """
        font-family: Gotham; color: #ffffff;background-color:#E30613; font-size: 16pt; border: 2px solid #ffffff;
        padding: 6px 20px;
        border-radius: 14px;"""

def style_img1_bg(img:str):
    return f"""
    QPushButton {{
        border: 2px solid #000000;
        border-radius: 20px;
        border-image: url("src/img/{img}") 0 0 0 0 stretch stretch;
        background-repeat: no-repeat;
        background-position: center;
        background-size: cover;
    }}
    QPushButton:hover {{
        border-radius: 20px;
        background-color: rgba(55,119,255,0.5);
        border: 8px solid #3777FF;
    }}
"""
style_date_selector = """
    QDateEdit {
        font-size: 11pt;
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
    }
    QCalendarWidget QToolButton {
        background-color: #ffffff;
        color: black;
    }

    QCalendarWidget QMenu::item{
        color:black;
        background-color: #ffffff;
    }
    
    QCalendarWidget QMenu::item:selected{
        color:#FFFFFF;
        background-color: #E30613;
    }
    
    QLabel {
        color: #333;
    }
"""
style_check_box = """QCheckBox {
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
        padding-left: 5px;
    }"""
style_spinBox = """
    QWidget {
        background-color: #FFF0E6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 10pt;
    }

    QSpinBox {
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
    }
"""
style_app_Dialogs = """
 
    QWidget {
        background-color: #FFF0E6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 10pt;
    }

    QLineEdit, QDateEdit, QComboBox,QSpinBox,QCheckBox,QDoubleSpinBox {
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
    }

    QCheckBox {
        padding-left: 5px;
    }

        
    QCalendarWidget QToolButton {
        background-color: #ffffff;
        color: black;
    }

    QCalendarWidget QMenu::item{
        color:black;
        background-color: #ffffff;
    }
    
    QCalendarWidget QMenu::item:selected{
        color:#FFFFFF;
        background-color: #E30613;
    }
    
    QLabel {
        color: #333;
    }
"""

style_check_box = """

    QWidget {
        background-color: #FFF0E6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 10pt;
    }

    QCheckBox {
        background-color: white;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
    }

    QCheckBox {
        padding-left: 5px;
    }

    QLabel {
        color: #333;
    }
"""

style_products_button = """
QPushButton {
    background-color: #fff5f0;       
    border: 2px solid #d43f3a;    
    border-radius: 12px;             
    padding: 10px 20px;          
    font-size: 14px;               
    font-weight: bold;
    color: #333333;               
}

QPushButton:hover {
    background-color: #d43f3a;       
    color: white;                 
}

"""
PADEL_COLOR_FG = "#1D6F63"
PADEL_COLOR_BG =  "#D1F2EB"
BEACHVOLLEY_COLOR_BG = "#FFF4CC"
BEACHVOLLEY_COLOR_FG = "#B28D00"
BEACHTENNIS_COLOR_BG = "#E6E6FA"
BEACHTENNIS_COLOR_FG = "#5D4E9A"
IN_PROGRESS_COLOR_BG = "#DFF7E4"
IN_PROGRESS_COLOR_FG = "#4C8C4A"

GREEN_COLOR_BG = "#C8E6C9"
GREEN_COLOR_FG = "#2E7D32"
YELLOW_COLOR_BG = "#FFF9C4"
YELLOW_COLOR_FG = "#F9A825"
RED_COLOR_BG = "#FFCDD2"
RED_COLOR_FG = "#C62828"
# EAF6FF bianco/grigio
# F5F5F5 bianco sporco
# FAFAFA avorio
# FFE6E6 rosa chiaro
# FFF0E6 albicocca chiaro