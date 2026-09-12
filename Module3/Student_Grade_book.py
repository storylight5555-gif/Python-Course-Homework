students = {
    "John": 94,
    "Alice": 88,
    "Bob": 91,
    "Eve": 95,
    "Charlie": 89,
    "David": 92
}
for student, grade in students.items():
    print(f"Grade: {grade}")
    

max_student = max(students, key=students.get)
min_student = min(students, key=students.get)
print("Highest Grade:", max_student, "with a grade of", students[max_student])
print("Lowest Grade:", min_student, "with a grade of", students[min_student])

chosen_student = input("Choose a student to see their grade: ")
if chosen_student in students:
    print(f"{chosen_student}'s grade is {students[chosen_student]}")
else:
    print("Student not found.")