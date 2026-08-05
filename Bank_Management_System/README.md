# 🏦 Bank Management System

A console-based **Bank Management System** built with **Python** using **Object-Oriented Programming (OOP)** principles and **JSON file storage** for persistent data. This project was built as a beginner-friendly yet professionally structured portfolio project, demonstrating core Python concepts through a real-world application.

---

## 📖 Project Overview

The Bank Management System simulates the core operations of a real bank through a simple command-line interface. Users can create accounts, deposit and withdraw funds, transfer money between accounts, and view detailed transaction histories — all while data is automatically saved to and loaded from a JSON file, so nothing is lost between sessions.

This project was designed to practice and showcase:
- Object-Oriented Programming (classes, objects, encapsulation)
- File handling and JSON serialization/deserialization
- Input validation and error handling
- Clean, professional CRUD (Create, Read, Update, Delete) application design

---

## ✨ Features

| # | Feature | Description |
|---|---------|--------------|
| 1 | **Create Account** | Auto-generates account numbers (`ACC1001`, `ACC1002`, ...), validates name/CNIC/phone, prevents duplicate CNIC |
| 2 | **View All Accounts** | Displays every account in a clean, formatted table |
| 3 | **Search Account** | Look up full account details using the account number |
| 4 | **Deposit Money** | Add funds to an account with automatic transaction logging |
| 5 | **Withdraw Money** | Withdraw funds with insufficient-balance protection |
| 6 | **Check Balance** | Instantly view an account's current balance |
| 7 | **Transfer Money** | Transfer funds between two accounts with full validation (sender/receiver existence, sufficient balance) and dual transaction logging |
| 8 | **Delete Account** | Permanently delete an account, with a confirmation prompt |
| 9 | **Transaction History** | View a full log of every transaction (type, amount, balance after, date & time) for an account |
| 10 | **Exit** | Automatically saves all data before closing the program |

### 🔒 Input Validation
- **Name** — alphabets and spaces only
- **CNIC** — must be exactly 13 digits
- **Phone Number** — must be 10 or 11 digits
- **Amounts** (deposit/withdraw/transfer) — must be positive numbers
- **Duplicate CNIC / Account Number** — automatically prevented

### 🛡️ Error Handling
The program uses `try/except` blocks throughout to gracefully handle invalid input, corrupted/missing JSON data, and unexpected runtime errors — the program never crashes on bad input.

---

## 🛠️ Technologies Used

- **Language:** Python 3
- **Core Concepts:** Object-Oriented Programming (Classes & Objects), Functions, Loops, Conditionals, Exception Handling
- **Data Storage:** JSON (`json` module) for persistent file-based storage
- **Standard Library Only:** `json`, `os`, `datetime` — no external dependencies required

---

## 📁 Folder Structure

```
Bank_Management_System/
│
├── main.py            # Complete application source code (Account & Bank classes, menu system)
├── accounts.json       # JSON data file — stores all account records (auto-created/updated)
└── README.md            # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tabbassamrabia68-code/Bank_Management_System.git
   cd Bank_Management_System
   ```

2. **Requirements:**
   - Python 3.7 or higher
   - No external/third-party libraries needed (uses only Python's standard library)

---

## ▶️ How to Run

Run the program from the terminal:

```bash
python3 main.py
```

On Windows, you may need:

```bash
python main.py
```

The program will automatically load any existing data from `accounts.json`. If it's your first time running the project, it will start with an empty account list and create the file automatically as you add accounts.

### Example Menu

```
==========================================
        BANK MANAGEMENT SYSTEM
==========================================
1. Create Account
2. View All Accounts
3. Search Account
4. Deposit Money
5. Withdraw Money
6. Check Balance
7. Transfer Money
8. Delete Account
9. Transaction History
10. Exit
==========================================
```

---

## 🚀 Future Improvements

- Build a **GUI version** using Tkinter or PyQt
- Add **PIN/password authentication** for account access
- Add **interest calculation** for savings accounts
- Export transaction history to **PDF/CSV**
- Add **multi-currency support**
- Migrate storage from JSON to a proper database (e.g., SQLite)
- Add unit tests using `pytest`

---

## 🎓 Learning Outcomes

Building this project helped reinforce the following Python and software engineering concepts:
- Designing and structuring a multi-class OOP application from scratch
- Reading from and writing to JSON files for persistent storage
- Writing robust input validation logic
- Handling exceptions gracefully to build resilient programs
- Structuring a project professionally for a GitHub portfolio
- Implementing real-world CRUD operations and business logic (like fund transfers)

---

## 👩‍💻 Author

**Rabia Tabbassam**

- GitHub: [tabbassamrabia68-code](https://github.com/tabbassamrabia68-code)
- LinkedIn: [rabia-tabbassam](https://www.linkedin.com/in/rabia-tabbassam/)

---

⭐ If you found this project helpful, consider giving it a star on GitHub!
