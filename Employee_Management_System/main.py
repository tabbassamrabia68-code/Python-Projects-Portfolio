import json
import os


# File location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "employees.json")


class Employee:
    def __init__(
        self,
        employee_id,
        name,
        age,
        phone,
        email,
        department,
        position,
        salary
    ):
        self.employee_id = employee_id
        self.name = name
        self.age = age
        self.phone = phone
        self.email = email
        self.department = department
        self.position = position
        self.salary = salary

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "age": self.age,
            "phone": self.phone,
            "email": self.email,
            "department": self.department,
            "position": self.position,
            "salary": self.salary
        }

    @staticmethod
    def from_dict(data):
        return Employee(
            data["employee_id"],
            data["name"],
            data["age"],
            data["phone"],
            data["email"],
            data["department"],
            data["position"],
            data["salary"]
        )


class EmployeeManagementSystem:

    def __init__(self):
        self.employees = {}
        self.load_data()

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    def load_data(self):
        try:
            if not os.path.exists(DATA_FILE):
                self.employees = {}
                self.save_data()
                return

            with open(DATA_FILE, "r") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                self.employees = {}
                return

            self.employees = {
                emp_id: Employee.from_dict(emp_data)
                for emp_id, emp_data in data.items()
            }

        except (json.JSONDecodeError, KeyError, TypeError):
            print("⚠️ employees.json contains invalid data.")
            self.employees = {}

        except Exception as e:
            print(f"⚠️ Error loading data: {e}")
            self.employees = {}

    # -----------------------------
    # SAVE DATA
    # -----------------------------
    def save_data(self):
        try:
            data = {
                emp_id: employee.to_dict()
                for emp_id, employee in self.employees.items()
            }

            with open(DATA_FILE, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(f"⚠️ Error saving data: {e}")

    # -----------------------------
    # GENERATE EMPLOYEE ID
    # -----------------------------
    def generate_employee_id(self):
        if not self.employees:
            return "EMP1001"

        numbers = []

        for employee_id in self.employees.keys():
            try:
                number = int(employee_id.replace("EMP", ""))
                numbers.append(number)
            except ValueError:
                continue

        if not numbers:
            return "EMP1001"

        return f"EMP{max(numbers) + 1}"

    # -----------------------------
    # ADD EMPLOYEE
    # -----------------------------
    def add_employee(self):

        print("\n========== ADD EMPLOYEE ==========")

        name = input("Enter employee name: ").strip()

        if not name:
            print("❌ Name cannot be empty.")
            return

        # Age validation
        while True:
            try:
                age = int(input("Enter age: "))

                if age < 18 or age > 100:
                    print("❌ Age must be between 18 and 100.")
                    continue

                break

            except ValueError:
                print("❌ Please enter a valid number.")

        phone = input("Enter phone number: ").strip()

        if not phone:
            print("❌ Phone number cannot be empty.")
            return

        email = input("Enter email: ").strip()

        if not email:
            print("❌ Email cannot be empty.")
            return

        department = input("Enter department: ").strip()

        if not department:
            print("❌ Department cannot be empty.")
            return

        position = input("Enter position: ").strip()

        if not position:
            print("❌ Position cannot be empty.")
            return

        # Salary validation
        while True:
            try:
                salary = float(input("Enter monthly salary: "))

                if salary < 0:
                    print("❌ Salary cannot be negative.")
                    continue

                break

            except ValueError:
                print("❌ Please enter a valid salary.")

        employee_id = self.generate_employee_id()

        employee = Employee(
            employee_id,
            name,
            age,
            phone,
            email,
            department,
            position,
            salary
        )

        self.employees[employee_id] = employee
        self.save_data()

        print("\n✅ Employee added successfully!")
        print(f"Employee ID: {employee_id}")

    # -----------------------------
    # VIEW ALL EMPLOYEES
    # -----------------------------
    def view_all_employees(self):

        print("\n========== ALL EMPLOYEES ==========")

        if not self.employees:
            print("❌ No employees found.")
            return

        for employee in self.employees.values():

            print("\n-----------------------------")
            print(f"Employee ID : {employee.employee_id}")
            print(f"Name        : {employee.name}")
            print(f"Age         : {employee.age}")
            print(f"Phone       : {employee.phone}")
            print(f"Email       : {employee.email}")
            print(f"Department  : {employee.department}")
            print(f"Position    : {employee.position}")
            print(f"Salary      : ${employee.salary:.2f}")

    # -----------------------------
    # SEARCH EMPLOYEE
    # -----------------------------
    def search_employee(self):

        print("\n========== SEARCH EMPLOYEE ==========")

        search = input(
            "Enter Employee ID or name to search: "
        ).strip().lower()

        found = False

        for employee in self.employees.values():

            if (
                employee.employee_id.lower() == search
                or search in employee.name.lower()
            ):

                print("\n-----------------------------")
                print(f"Employee ID : {employee.employee_id}")
                print(f"Name        : {employee.name}")
                print(f"Age         : {employee.age}")
                print(f"Phone       : {employee.phone}")
                print(f"Email       : {employee.email}")
                print(f"Department  : {employee.department}")
                print(f"Position    : {employee.position}")
                print(f"Salary      : ${employee.salary:.2f}")

                found = True

        if not found:
            print("❌ Employee not found.")

    # -----------------------------
    # UPDATE EMPLOYEE
    # -----------------------------
    def update_employee(self):

        print("\n========== UPDATE EMPLOYEE ==========")

        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id not in self.employees:
            print("❌ Employee not found.")
            return

        employee = self.employees[employee_id]

        print("\nPress Enter to keep the current value.")

        name = input(f"Name [{employee.name}]: ").strip()

        if name:
            employee.name = name

        age_input = input(f"Age [{employee.age}]: ").strip()

        if age_input:
            try:
                age = int(age_input)

                if 18 <= age <= 100:
                    employee.age = age
                else:
                    print("❌ Invalid age. Old age kept.")

            except ValueError:
                print("❌ Invalid age. Old age kept.")

        phone = input(f"Phone [{employee.phone}]: ").strip()

        if phone:
            employee.phone = phone

        email = input(f"Email [{employee.email}]: ").strip()

        if email:
            employee.email = email

        department = input(
            f"Department [{employee.department}]: "
        ).strip()

        if department:
            employee.department = department

        position = input(
            f"Position [{employee.position}]: "
        ).strip()

        if position:
            employee.position = position

        salary_input = input(
            f"Salary [{employee.salary}]: "
        ).strip()

        if salary_input:

            try:
                salary = float(salary_input)

                if salary >= 0:
                    employee.salary = salary
                else:
                    print("❌ Salary cannot be negative.")

            except ValueError:
                print("❌ Invalid salary. Old salary kept.")

        self.save_data()

        print("✅ Employee updated successfully!")

    # -----------------------------
    # DELETE EMPLOYEE
    # -----------------------------
    def delete_employee(self):

        print("\n========== DELETE EMPLOYEE ==========")

        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id not in self.employees:
            print("❌ Employee not found.")
            return

        employee = self.employees[employee_id]

        print(f"\nEmployee: {employee.name}")
        print(f"Department: {employee.department}")

        confirm = input(
            "Are you sure you want to delete this employee? (y/n): "
        ).strip().lower()

        if confirm == "y":

            del self.employees[employee_id]
            self.save_data()

            print("✅ Employee deleted successfully!")

        else:
            print("❌ Delete operation cancelled.")

    # -----------------------------
    # CALCULATE SALARY
    # -----------------------------
    def calculate_salary(self):

        print("\n========== SALARY CALCULATOR ==========")

        employee_id = input("Enter Employee ID: ").strip().upper()

        if employee_id not in self.employees:
            print("❌ Employee not found.")
            return

        employee = self.employees[employee_id]

        basic_salary = employee.salary

        bonus = basic_salary * 0.10
        tax = basic_salary * 0.05

        net_salary = basic_salary + bonus - tax

        print("\n========== SALARY DETAILS ==========")
        print(f"Employee       : {employee.name}")
        print(f"Employee ID    : {employee.employee_id}")
        print(f"Basic Salary   : ${basic_salary:.2f}")
        print(f"Bonus (10%)    : ${bonus:.2f}")
        print(f"Tax (5%)       : ${tax:.2f}")
        print(f"Net Salary     : ${net_salary:.2f}")

    # -----------------------------
    # DEPARTMENT EMPLOYEES
    # -----------------------------
    def department_employees(self):

        print("\n========== DEPARTMENT SEARCH ==========")

        department = input(
            "Enter department name: "
        ).strip().lower()

        found = False

        for employee in self.employees.values():

            if employee.department.lower() == department:

                print("\n-----------------------------")
                print(f"Employee ID : {employee.employee_id}")
                print(f"Name        : {employee.name}")
                print(f"Position    : {employee.position}")
                print(f"Salary      : ${employee.salary:.2f}")

                found = True

        if not found:
            print("❌ No employees found in this department.")

    # -----------------------------
    # MAIN MENU
    # -----------------------------
    def menu(self):

        while True:

            print("\n")
            print("======================================")
            print("      EMPLOYEE MANAGEMENT SYSTEM")
            print("======================================")
            print("1. Add Employee")
            print("2. View All Employees")
            print("3. Search Employee")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Calculate Salary")
            print("7. View Department Employees")
            print("8. Exit")
            print("======================================")

            choice = input("Enter your choice (1-8): ").strip()

            if choice == "1":
                self.add_employee()

            elif choice == "2":
                self.view_all_employees()

            elif choice == "3":
                self.search_employee()

            elif choice == "4":
                self.update_employee()

            elif choice == "5":
                self.delete_employee()

            elif choice == "6":
                self.calculate_salary()

            elif choice == "7":
                self.department_employees()

            elif choice == "8":
                print("\n👋 Thank you for using Employee Management System!")
                break

            else:
                print("❌ Invalid choice. Please select 1-8.")


# -----------------------------
# PROGRAM START
# -----------------------------

if __name__ == "__main__":
    system = EmployeeManagementSystem()
    system.menu()