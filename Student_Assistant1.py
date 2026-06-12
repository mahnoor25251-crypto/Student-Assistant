students = {}
timetables = {}
marks_data = {}

ALLOWED_DEPTS = ["computer science", "data science", "cyber security", "it"]
ALLOWED_SUBJECTS = ["programming fundamental", "ict", "applied physics", "english", "quran"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# ---------------- Performance Calculation ----------------
def get_performance(roll):
    #Calculates average marks and grade for a student.
    if roll not in marks_data or not marks_data[roll]:#if roll not exist in marks_data value return
        return 0, "N/A"

    marks_list = marks_data[roll].values() # built in method
    avg = sum(marks_list) / len(marks_list)

    if avg >= 90:
        grade = "A+"
    elif avg >= 80:
        grade = "A"
    elif avg >= 70: 
        grade = "B"
    elif avg >= 60:
        grade = "C"
    else:
        grade = "Fail"

    return round(avg, 2), grade

# ---------------- Bulk Student Registration ----------------
def add_students_bulk():
    while True:
        print("\n--- Student Registration ---")
        roll = input("Enter Roll Number (exactly 6 digits) or 'stop': ").strip()

        if roll.lower() == 'stop':
            break

        if not roll.isdigit(): # digit validation
            print("Error: Roll number must contain numbers only!")
            continue

        if len(roll) != 6: # numbers validations
            print("Error: Roll number must be exactly 6 digits!")
            continue

        while True:
            name = input("Enter Student Name: ").strip()
            if name and name.replace(" ", "").isalpha(): # only letters 
                break
            else:
                print("Error: Name must contain only letters and cannot be empty!")

        while True:
            print("Choose Dept:", ", ".join(ALLOWED_DEPTS))
            dept = input("Department: ").strip().lower()
            if dept in [d.lower() for d in ALLOWED_DEPTS]: # validation
                students[roll] = {"name": name, "department": dept.upper()}  # Save in uppercase
                break
            else:
                print("Error: Invalid department!")

        # -------- Add Timetable --------
        while True:
            choice = input(f"Add timetable for {name}? (y/n): ").lower().strip()
            if choice == 'y': # choice validation
                while True:
                    day = input("Enter Day: ").strip().lower()
                    if day in DAYS:
                        while True:
                            print("Subjects:", ", ".join(ALLOWED_SUBJECTS))
                            subj = input("Subject: ").strip().lower()
                            if subj in ALLOWED_SUBJECTS:
                                if roll not in timetables:
                                    timetables[roll] = {}
                                timetables[roll][day.capitalize()] = subj.upper()
                                break
                            else:
                                print("Error: Subject not allowed!")
                        break
                    else:
                        print("Error: Invalid day!")  
                break
            elif choice == 'n':
                break
            else:
                print("Error: Use y or n only.")

        # -------- Add Marks --------
        while True:
            choice = input(f"Add marks for {name}? (y/n): ").lower().strip()
            if choice == 'y': # choice validation
                while True:
                    print("Subjects:", ", ".join(ALLOWED_SUBJECTS))
                    m_subj = input("Subject: ").strip().lower()
                    if m_subj in ALLOWED_SUBJECTS: # validation
                        try:
                            m_val = int(input("Enter Marks (0-100): "))
                            if 0 <= m_val <= 100:
                                if roll not in marks_data: # validation
                                    marks_data[roll] = {}
                                marks_data[roll][m_subj.upper()] = m_val
                                break
                            else:
                                print("Error: Marks must be between 0 and 100.")
                        except ValueError:
                            print("Error: Numbers only.")
                    else:
                        print("Error: Subject not allowed!")
                break
            elif choice == 'n': # choice validation
                break
            else:
                print("Error: Use y or n only.")

        print(f"Student saved successfully: {name}")

# ---------------- Search Student by Roll ----------------
def search_by_roll():
    roll = input("\nEnter Roll Number: ").strip()
    if roll in students:
        s = students[roll]
        avg, grade = get_performance(roll)

        print("\n" + "=" * 45)
        print(f"STUDENT: {s['name'].upper()} | ROLL: {roll}")
        print(f"DEPT: {s['department'].upper()}")
        print(f"SCHEDULE: {timetables.get(roll, 'Not Set')}")
        print("MARKS:")
        if roll in marks_data and marks_data[roll]:
            for subj, marks in marks_data[roll].items():
                print(f"  {subj}: {marks}")
        else:
            print("  Not Set")
        print(f"RESULT: {avg}% - {grade}")
        print("=" * 45)
    else:
        print("Error: Roll number not found.")

# ---------------- Filter Students by Department ----------------
def filter_by_department():
    print("Available Depts:", ", ".join(ALLOWED_DEPTS))
    target_dept = input("Enter Department: ").strip().upper()

    if target_dept not in [d.upper() for d in ALLOWED_DEPTS]: 
        print("Error: Invalid department.")
        return

    print(f"\nStudents in {target_dept}:")
    found = False
    for roll, info in students.items():
        if info['department'] == target_dept: # allow department  
            
            avg, grade = get_performance(roll)
            print(f"Name: {info['name']} | Roll: {roll} | Result: {avg}% ({grade})")
            found = True

    if not found:
        print("No students found.")

# ---------------- Save to File (Append Mode) ----------------
def save_to_file():
    filename = "university_records.txt"

    # Check if file exists and is empty
    try:
        with open(filename, "r") as f:
            existing_data = f.read().strip()
    except FileNotFoundError:
        existing_data = ""

    with open(filename, "a") as f:
        # Add header only if file is empty
        if not existing_data:
            f.write("OFFICIAL STUDENT RECORDS\n")
            f.write("=" * 25 + "\n\n")

        for r in students:
            avg, g = get_performance(r)
            f.write(
                f"NAME: {students[r]['name']} | "
                f"ROLL: {r} | "
                f"DEPT: {students[r]['department']} | "
                f"RESULT: {avg}% ({g})\n"
            )

    print(f"Success! Data appended in {filename}")

# ---------------- Main Menu ----------------
def main():
    while True:
        print("\n===== UNIVERSITY SYSTEM =====")
        print("1. Register Students (Bulk)")
        print("2. Search Student by Roll No")
        print("3. Filter Students by Department")
        print("4. Save All to File")
        print("5. Exit")

        choice = input("Select Option (1-5): ").strip()
        if choice == '1':
            add_students_bulk()
        elif choice == '2':
            search_by_roll()
        elif choice == '3':
            filter_by_department()
        elif choice == '4':
            save_to_file()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()






