import json
import os

FILE_NAME = "Student_Management_System/students.json"


class Student:
    def __init__(self, student_id, name, age, course):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course
        }

    def display(self):
        print("-" * 40)
        print(f"Student ID : {self.student_id}")
        print(f"Name       : {self.name}")
        print(f"Age        : {self.age}")
        print(f"Course     : {self.course}")
        print("-" * 40)


students = []


def load_students():
    global students

    students.clear()

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)

                for item in data:
                    students.append(
                        Student(
                            item["student_id"],
                            item["name"],
                            item["age"],
                            item["course"]
                        )
                    )
        except:
            pass


def save_students():
    data = []

    for student in students:
        data.append(student.to_dict())

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def add_student():

    student_id = input("Enter Student ID: ")

    for student in students:
        if student.student_id == student_id:
            print("Student ID already exists.")
            return

    name = input("Enter Student Name: ")
    age = input("Enter Student Age: ")
    course = input("Enter Course: ")

    students.append(Student(student_id, name, age, course))

    save_students()

    print("Student added successfully!")


def view_students():

    if len(students) == 0:
        print("No student records found.")
        return

    print("\nStudent Records")

    for student in students:
        student.display()


def search_student():

    student_id = input("Enter Student ID: ")

    for student in students:
        if student.student_id == student_id:
            print("\nStudent Found")
            student.display()
            return

    print("Student not found.")


def update_student():

    student_id = input("Enter Student ID: ")

    for student in students:

        if student.student_id == student_id:

            student.name = input("Enter New Name: ")
            student.age = input("Enter New Age: ")
            student.course = input("Enter New Course: ")

            save_students()

            print("Student updated successfully!")

            return

    print("Student not found.")


def delete_student():

    student_id = input("Enter Student ID: ")

    for student in students:

        if student.student_id == student_id:

            students.remove(student)

            save_students()

            print("Student deleted successfully!")

            return

    print("Student not found.")


load_students()

while True:

    print("\n" + "=" * 45)
    print("      STUDENT MANAGEMENT SYSTEM")
    print("=" * 45)

    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        print("Thank you for using Student Management System.")
        break

    else:
        print("Invalid choice.")