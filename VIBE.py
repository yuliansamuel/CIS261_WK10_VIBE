#Samuel Barco
#CIS261
#WK10 VIBE Coding
#This program was created with assistance from VIBE/GitHub Copilot Agent.
#The code was reviewed, tested, and corrected to meet the Week 10 lab requirements.

import os

FILE_NAME = "student_grades.txt"


def load_students(filename):
    students = []
    if not os.path.isfile(filename):
        return students

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 7:
                    continue

                name, student_id, test1, test2, test3, average, grade = parts
                try:
                    student = {
                        "name": name,
                        "id": student_id,
                        "test1": float(test1),
                        "test2": float(test2),
                        "test3": float(test3),
                        "average": float(average),
                        "grade": grade,
                    }
                    students.append(student)
                except ValueError:
                    continue
    except IOError as error:
        print(f"Error loading records from {filename}: {error}")
    return students


def save_students(filename, students):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                line = (
                    f"{student['name']}|{student['id']}|"
                    f"{student['test1']:.2f}|{student['test2']:.2f}|{student['test3']:.2f}|"
                    f"{student['average']:.2f}|{student['grade']}\n"
                )
                file.write(line)
        print(f"Saved {len(students)} student record(s) to {filename}.")
    except IOError as error:
        print(f"Error saving records to {filename}: {error}")


def calculate_average(test1, test2, test3):
    return (test1 + test2 + test3) / 3


def calculate_grade(average):
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def get_input(prompt):
    value = input(prompt).strip()
    if value.upper() == "ESC":
        raise KeyboardInterrupt
    return value


def get_student_score(prompt):
    while True:
        try:
            value = get_input(prompt)
            score = float(value)
            if 0 <= score <= 100:
                return score
            print("Score must be between 0 and 100. Please try again.")
        except ValueError:
            print("Invalid entry. Please enter a numeric score.")


def add_student(students):
    try:
        name = get_input("Enter student name (or ESC to exit): ")
        student_id = get_input("Enter student ID (or ESC to exit): ")
        test1 = get_student_score("Enter score for Test 1 (0-100): ")
        test2 = get_student_score("Enter score for Test 2 (0-100): ")
        test3 = get_student_score("Enter score for Test 3 (0-100): ")

        average = calculate_average(test1, test2, test3)
        grade = calculate_grade(average)

        student = {
            "name": name,
            "id": student_id,
            "test1": test1,
            "test2": test2,
            "test3": test3,
            "average": average,
            "grade": grade,
        }
        students.append(student)
        print(f"Added student: {name} with average {average:.2f} and grade {grade}.")
    except KeyboardInterrupt:
        print("\nExit requested. Returning to menu.")


def display_students(students):
    if not students:
        print("No student records available.")
        return

    header = (
        f"{'Name':<20} {'ID':<12} {'Test1':>7} {'Test2':>7} {'Test3':>7} "
        f"{'Average':>8} {'Grade':>6}"
    )
    print(header)
    print("-" * len(header))

    for s in students:
        print(
            f"{s['name']:<20} {s['id']:<12} "
            f"{s['test1']:>7.2f} {s['test2']:>7.2f} {s['test3']:>7.2f} "
            f"{s['average']:>8.2f} {s['grade']:>6}"
        )


def show_statistics(students):
    if not students:
        print("No student records available for statistics.")
        return

    averages = [student["average"] for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_avg = sum(averages) / len(averages)

    highest_students = [s["name"] for s in students if s["average"] == highest]
    lowest_students = [s["name"] for s in students if s["average"] == lowest]

    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for student in students:
        grade = student.get("grade", "")
        if grade in grade_counts:
            grade_counts[grade] += 1

    print(f"Class average:   {class_avg:.2f}")
    print(f"Highest average: {highest:.2f} ({', '.join(highest_students)})")
    print(f"Lowest average:  {lowest:.2f} ({', '.join(lowest_students)})")
    print("\nGrade Distribution:")
    for grade in ["A", "B", "C", "D", "F"]:
        count = grade_counts[grade]
        if count > 0:
            print(f"{grade}: {count} student(s)")


def search_student(students):
    if not students:
        print("No student records available to search.")
        return

    name_query = input("Enter student name to search (case-insensitive, or ESC to exit): ").strip()
    if name_query.upper() == "ESC":
        print("Search cancelled.")
        return

    matches = [s for s in students if name_query.lower() in s["name"].lower()]
    if not matches:
        print(f"No student found matching '{name_query}'.")
        return

    print(f"Found {len(matches)} record(s):")
    display_students(matches)


def display_menu():
    print("\nStudent Grade Calculator")
    print("1. Add new student record")
    print("2. Display all students")
    print("3. Show class statistics")
    print("4. Search for student by name")
    print("5. Save and exit (or type ESC at any prompt)")


def main():
    students = load_students(FILE_NAME)
    if students:
        print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")
    else:
        print("No saved records found. Starting with an empty list.")

    while True:
        display_menu()
        choice = input("Choose an option (1-5) or ESC to exit: ").strip()
        if choice.upper() == "ESC" or choice == "5":
            save_students(FILE_NAME, students)
            print("Goodbye.")
            break
        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            show_statistics(students)
        elif choice == "4":
            search_student(students)
        else:
            print("Invalid selection. Please enter 1-5 or ESC.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Saving records before exit.")
        save_students(FILE_NAME, load_students(FILE_NAME))
