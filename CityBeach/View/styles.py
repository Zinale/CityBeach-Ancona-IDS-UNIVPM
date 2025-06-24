def style_input_bar_white()->str:
    return """
    QLineEdit {
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #CCCCCC;
        border-radius: 6px;
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
        border-radius: 6px;
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
def style_QButton_white_18Gotham(font:str)->str:
    return f"""
    QPushButton {{
        font-family: "{font}"; font-size: 18pt;
        background-color: #FFFFFF;
        color: #444444;
        border: 1px solid #E30613;
        border-radius: 14px;
        padding: 6px 20px;
    }}
    QPushButton:hover {{
        background-color: #EEEEEE;
        border: 2px solid #E30613;
    }}
"""
style_blackText = """
    QLabel, QFrame {
        color: #000000;
    }
"""

style_text_gotham_b = """
        font-family: Gotham; color: #444444;font-size: 16pt;"""

style_text_red_on_white = """
        font-family: Gotham; color: #E30613;background-color:#ffffff; font-size: 16pt; border: 2px solid #E30613;
        padding: 6px 20px;
        border-radius: 14px;"""

style_text_white_on_red = """
        font-family: Gotham; color: #ffffff;background-color:#E30613; font-size: 16pt; border: 2px solid #ffffff;
        padding: 6px 20px;
        border-radius: 14px;"""

# da fare per ogni button
style_img1_bg = """
    QPushButton {
        border: 1px solid #000000;
        border-radius: 14px;
        background-image: url(src/img/Baby.tux.sit-800x800.png);
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
    }
    QPushButton:hover {
        background-color: rgba(0, 0, 0, 30);
        border: 2px solid #3777FF;
    }
"""

style_app_Dialogs = """
 
    QWidget {
        background-color: #FFF0E6;
        font-family: 'Segoe UI', sans-serif;
        font-size: 10pt;
    }

    QLineEdit, QDateEdit, QComboBox {
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

# EAF6FF bianco/grigio
# F5F5F5 bianco sporco
# FAFAFA avorio
# FFE6E6 rosa chiaro
# FFF0E6 albicocca chiaro