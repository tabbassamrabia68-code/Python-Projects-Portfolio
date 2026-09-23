# Employee Management System

A console-based Employee Management System developed using Python and Object-Oriented Programming (OOP). This project provides a simple and structured way to manage employee records, perform CRUD operations, calculate salaries, search employees, update information, delete records, and organize employees by department.

## Project Overview

The Employee Management System is a Python application designed to simulate a basic employee management solution.

The application allows users to manage employee information through an interactive command-line interface. Employee records are stored in a JSON file, allowing the data to remain available after the application is closed.

This project demonstrates practical use of Python programming, OOP, JSON data storage, file handling, CRUD operations, input validation, and exception handling.

## Features

### Add Employee
- Add a new employee
- Automatically generate a unique Employee ID
- Store employee name, age, phone, email, department, position, and salary

Example Employee IDs:

- EMP1001
- EMP1002
- EMP1003

### View All Employees
Display all registered employees with their:
- Employee ID
- Name
- Age
- Phone
- Email
- Department
- Position
- Salary

### Search Employee
Search for an employee using:
- Employee ID
- Employee Name
- Phone Number
- Email Address

### Update Employee
Update existing employee information including:
- Name
- Age
- Phone
- Email
- Department
- Position
- Salary

### Delete Employee
Delete an employee record using the Employee ID.

The system verifies the employee before deleting the record.

### Calculate Salary
The system calculates employee salary using a basic bonus and tax calculation.

Salary formula:

```text
Bonus = 10% of Basic Salary
Tax = 5% of Basic Salary
Net Salary = Basic Salary + Bonus - Tax

Employee_Management_System/
│
├── main.py
├── employees.json
└── README.md

employees.json
========================================
       EMPLOYEE MANAGEMENT SYSTEM
========================================

1. Add Employee
2. View All Employees
3. Search Employee
4. Update Employee
5. Delete Employee
6. Calculate Salary
7. View Department Employees
8. Exit

Enter your choice:1

{
    "EMP1001": {
        "name": "Ali Khan",
        "age": 25,
        "phone": "03001234567",
        "email": "ali@example.com",
        "department": "IT",
        "position": "Software Developer",
        "salary": 50000
    }
}

