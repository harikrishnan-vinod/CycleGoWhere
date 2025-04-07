# 🚴‍♀️ CycleGoWhere! (2006‑SCSC‑A3)

> Software Engineering Project \
> Nanyang Technological Unviersity \
> Group 3

## Our Team

| Name               | Github ID                                                   |
| ------------------ | ----------------------------------------------------------- |
| Lim En Jia         | [@enjiaaaa](https://github.com/enjiaaaa)                    |
| Bryan Goh Wei Hao  | [@raccocoder](https://github.com/raccocoder)                |
| Ethan Yew          | [@eyyt2309](https://github.com/eyyt2309)                    |
| Harikrishnan Vinod | [@harikrishnanvinod](https://github.com/harikrishnan-vinod) |
| Chin Hui Qi Cheryl | [@cherylchq](https://github.com/cherylchq)                  |

---

## 📋 Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Functional Requirements](#functional-requirements)
7. [Non‑Functional Requirements](#non-functional-requirements)
8. [Data Dictionary](#data-dictionary)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact](#contact)

---

## 🧐 Introduction

Our mission is to empower amateur cyclists with a seamless and stress‑free riding experience. **CycleGoWhere!** lets you:

- **Plan** safe, scenic routes using Singapore’s park connector network
- **Discover** nearby amenities like `Water Coolers`, `Bike Repair Shops`, and `Bike Parking Spots`
- **Save** your favourite routes

This project supports Singapore’s Smart Nation initiative by leveraging publicly available government data and modern web technologies.

---

## ✨ Features

- **Authentication**: `User Login`, `Create Account`, `Google Login`, `Forgot Password`,
- **Route Planning**: Interactive `Search Bar` + `Map` with auto‑complete
- **Filters**: Toggle `Water Coolers`, `Bike Repair`, `Bike Parks` within 500 m of your path
- **Turn‑by‑Turn Navigation**: Real‑time tracking & guidance
- **Activity Logging**: Name, annotate, and save your rides
- **Profile Dashboard**: Daily/weekly/monthly stats, ride history
- **Saved Routes**: Start or “unsave” previously saved routes
- **Settings**: Update username, email, password, profile picture, or log out

---

## 🛠 Tech Stack

- **Frontend**: `React` • `Vite` • `react-router-dom` • `lucide-react`
- **Backend**: `Python` • `Flask`
- **Database**: `Firestore` (via Google Cloud)
- **Map & Routing**: `OneMap API`
- **Authentication**: Firebase Authentication

---

## ⚙️ Installation

### 1. Clone the Repo

```bash
git clone https://github.com/your‑org/2006-SCSC-A3.git
cd 2006-SCSC-A3
```

### 2. Run Frontend

```sh
cd .src/frontend
npm install react-router-dom
npm install lucide-react
npm install
npm run dev
```

### 3. Run Backend

```sh
cd .src/backend
python app.py
```
