# 🏖️ CityBeach Ancona

[![en](https://img.shields.io/badge/lang-English-blue)](README.md)
[![it](https://img.shields.io/badge/lang-Italiano-green)](README.it.md)

CityBeach Ancona is a **desktop management software** for the **Palabeach** sports facility in Ancona, developed as part of the **Software Engineering (IDS)** course at **Università Politecnica delle Marche (UNIVPM)**.  

<p align="center">
  <img src="CityBeach/src/img/logo.png" width="300" alt="logo">
</p>

The application is currently under active development and follows the **MVC (Model-View-Controller)** architecture.  
The graphical interface is built with **PyQt6**.  

---

## 📌 Overview

CityBeach is designed to simplify the daily operations of a beach sports facility.  
It allows administrators and staff to manage:

- 👤 Users and players  
- 🏐 Sports equipment inventory  
- 📆 Reservations and usage tracking  
- 🏅 Field and locker room occupancy monitoring  
- 🍔 **Refreshment area** with product and order management  

> ⚠️ The software is a university project and is **not ready for production use**.  

---

## 🖥️ Technologies

- **Python 3.13**
- **PyQt6**
- **Pickle**
- **MatPlotLib**
- **Object-Oriented Programming (OOP)**
- **MVC Architecture**
- **Custom Fonts (Gotham)**
- **Custom Images (Freepik License)**

> No database integration yet.  
> Data is managed in memory or via static Python objects.  

---

## 🗂️ Project Structure
```
CityBeach/
├── main.py
├── paths.py
├── requirements.txt
├── Controller/
│   ├── BookingsController.py
│   ├── FieldsController.py
│   ├── LockersController.py
│   ├── PlayersController.py
│   ├── RestaurantController.py
│   ├── SportsEquipmentController.py
│   └── UsersController.py
├── Model/
│   ├── Booking.py
│   ├── Data.py
│   ├── Field.py
│   ├── Gender.py
│   ├── Locker.py
│   ├── Order.py
│   ├── Player.py
│   ├── Product.py
│   ├── SportsCategory.py
│   ├── SportsEquipment.py
│   └── User.py
├── src/
│   └── fonts/
│       ├── Gotham-Black.otf
│       ├── Gotham-Thin.otf
│       ├── Gotham-ThinItalic.otf
│       ├── Gotham-UltraItalic.otf
│       ├── GothamBold.ttf
│       ├── GothamBoldItalic.ttf
│       ├── GothamBook.ttf
│       ├── GothamBookItalic.ttf
│       ├── GothamLight.ttf
│       ├── GothamLightItalic.ttf
│       └── GothamMediumItalic.ttf
├── UnitTestCase/
│   ├── BookingTestCase.py
│   ├── RestaurantTestCase.py
│   └── UserTestCase.py
└── View/
    ├── AttrezzaturaSportiva_ui.py
    ├── Booking_ui.py
    ├── DateTimeLabel.py
    ├── Employee_ui.py
    ├── Fields_Locker_ui.py
    ├── Login_ui.py
    ├── Main_ui.py
    ├── Player_ui.py
    ├── Restaurant_ui.py
    ├── styles.py
    ├── topBar.py
    └── View.py
```

---

## 🚧 Development Status

| Feature                                       | Status        |
| --------------------------------------------- | ------------- |
| Basic UI structure                            | ✅ Done        |
| MVC pattern                                   | ✅ Done        |
| Equipment and user management                 | ✅ Done        |
| Data persistence (local `data.pkl` file)      | ✅ Done        |
| Authentication and roles                      | ✅ Done        |
| Field and locker management                   | ✅ Done        |
| Booking system                                | ✅ Done        |
| Sports equipment management                   | ✅ Done        |
| Refreshment area management                   | ✅ Done        |
| Final styling & responsive layout             | 🔄 In progress |
| Report generation (PDF)                       | 🔄 In progress |

---

## 📖 How to Use

### ‼️ First Login
Default admin credentials on first run:
```
👤 Username: admin
🔑 Password: admin
```
> ⛔️ The "admin" account always exists and cannot be deleted or modified.

### 📋 Functional Panels

- **Employees Panel**  
  Manage all system users (staff and non-staff).  
  - New users start with an empty password (`""`).  
  - Administrators can reset passwords but cannot retrieve them.  

- **Players Panel**  
  Manage player profiles.  
  Bookings require a registered player.  

- **Fields & Lockers Panel**  
  Manage available fields and locker rooms.  
  It is possible to generate some **graphs** that show the progress of the activity
  - **Static view:** overview with main characteristics and statistical charts.  
  - **Dynamic view:** select a date → see field/locker status by time slot.  

  > Supported sports: Beach Volleyball, Padel, Beach Tennis  

- **Bookings Panel**  
  Create new bookings (**today or future dates only**).  
  Booking status is automatically updated:  
  📅 **REGISTERED → IN PROGRESS → COMPLETED**  

- **Restaurant Panel (Refreshment Area)**  
  Manage products by category:  
  - 🥤 Beverages  
  - 🍷 Alcohol  
  - 🍔 Food  
  - 🍫 Snacks  

  Products can be added to **orders**, which are then viewable in a dedicated section.  

---

## 💻 Some Mockup
<p align="center">
  <table>
    <tr>
      <td><img src="docs/Mockup/login.png" width="350" alt="login"  /></td>
      <td><img src="docs/Mockup/main.png" width="350" alt="main"  /></td>
      <td><img src="docs/Mockup/giocatori.png" width="350" alt="giocatori"  /></td>
    </tr>
  </table>
  <table>
    <tr>
      <td><img src="docs/Mockup/campiSpogliatoiDinamica.png" width="350" alt="campi-spogliatoi"  /></td>
      <td><img src="docs/Mockup/areaRistoro.png" width="350" alt="Ristoro"  /></td>
    </tr>
  </table>
</p>

---

## 📄 License

This project is developed for academic purposes and is not yet distributed under a specific open-source license.  
License terms will be added later.  

---

## 📬 Contact

For questions, suggestions, or collaboration:  

- 📧 s1116714@studenti.univpm.it  | Alessandro Zingaretti  
- 📧 s1118107@studenti.univpm.it  | Lorenzo Rossetti  
- 📧 s1115276@studenti.univpm.it  | Tomas Mosciatti  
