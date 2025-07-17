# 🏖️🏐   CityBeach Ancona – Management System ​🗂️📆

CityBeach Ancona is a desktop-based management software for the **Palabeach** in Ancona, developed as part of the **Software Engineering (IDS)** course at **Università Politecnica delle Marche (UNIVPM)**.

<p align="center">
  <img src="CityBeach\src\img\logo.png" width="300" alt="logo">
</p>

This application is currently under active development and follows the **MVC** (Model-View-Controller) architecture. The graphical interface is built using **PyQt-6**.

---

## 📌 Overview

CityBeach is designed to simplify the day-to-day operations of a beach sports facility. It allows administrators and staff to manage:a

- 👤 Users and players  
- 🏐 Sports equipment inventory  
- 📆 Reservations and usage tracking
- 🏅 Field and changing room occupancy monitoring to prevent overcrowding
- 🍔 In-house refreshment area management: available products and order tracking

The software is being developed as a course project and is not yet ready for production use.

---

## 🖥️ Technologies

- **Python 3.13**
- **PyQt6**
- **Pickle**
- **Object-Oriented Programming**
- **MVC Architecture**
- **Custom Fonts (Gotham)**
- **Custom Images (Freepik License)

> Note: No database integration is present yet. Data is handled in-memory or through static Python objects.

---

## 🗂️ Project Structure
```
Directory structure:
└── sf_CityBeach/
    ├── main.py
    ├── paths.py
    ├── requirements.txt
    ├── Controller/
    │   ├── AttrrezzaturaSportivaController.py
    │   ├── PlayersController.py
    │   └── UsersController.py
    ├── examples/
    │   ├── QSplitter.py
    │   ├── QTableWidget.py
    │   └── QTreeWidget.py
    ├── Model/
    │   ├── Article.py
    │   ├── Data.py
    │   ├── EquipmentType.py
    │   ├── Gender.py
    │   ├── Player.py
    │   ├── SportsCategory.py
    │   ├── SportsEquipment.py
    │   └── User.py
    ├── src/
    │   ├── fonts/
    │   │   ├── Gotham-Black.otf
    │   │   ├── Gotham-Thin.otf
    │   │   ├── Gotham-ThinItalic.otf
    │   │   ├── Gotham-UltraItalic.otf
    │   │   ├── GothamBold.ttf
    │   │   ├── GothamBoldItalic.ttf
    │   │   ├── GothamBook.ttf
    │   │   ├── GothamBookItalic.ttf
    │   │   ├── GothamLight.ttf
    │   │   ├── GothamLightItalic.ttf
    │   │   └── GothamMediumItalic.ttf
    │   └── img/
    │       ├── Baby.tux.sit-800x800.png
    │       ├── logo.png
    │       ├── players.png
    │       ├── sports_equip.png
    │       └── staff.png
    └── View/
        ├── AttrezzaturaSportiva_ui.py
        ├── DateTimeLabel.py
        ├── Dipendenti_ui.py
        ├── Login_ui.py
        ├── Main_ui.py
        ├── Player_ui.py
        ├── styles.py
        ├── topBar.py
        └── View.py
```

## 🚧 Development Status
| Feature                                       | Status        |
| ----------------------------------            | ------------- |
| Basic UI structure                            | ✅ Done        |
| MVC pattern                                   | ✅ Done        |
| Equipment and user management                 | ✅ Done       |
| Data persistence (local `data.pkl` file)      | ✅ Done    |
| Authentication and roles                      | ✅ Done    |
| Field and changing room management system     | 🔧 Planned    |
| Reservation system                            | 🔧 Planned    |
| Refreshment area management                   | 🔧 Planned    |
| Final styling & responsive layout             | 🔧 Planned    |
| Report generation (PDF)                       | 🔄 In progress    |

---

## 📄 License

This project is currently developed for academic purposes and is not yet distributed under a specific open-source license. Licensing terms will be added later.

## 📬 Contact

For questions, suggestions, or collaboration, please contact:

- 📧 s1116714@studenti.univpm.it  | Alessandro Zingaretti
- 📧 s1118107@studenti.univpm.it  | Lorenzo Rossetti
- 📧 s1115276@studenti.univpm.it  | Tomas Mosciatti


