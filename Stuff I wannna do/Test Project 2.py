studentbook = [
    {"name": "John", "score": 95},
    {"name": "Rose", "score": 88},
    {"name": "Micheal", "score": 92},
    {"name": "Sara", "score": 90},
    {"name": "Dave", "score": 85},
]
total_score = 0
for student in studentbook:
    total_score += student["score"]
    print(student["name"], "scored", student["score"] / 2, "points")
print("Total score:", total_score / 2)
print("Top student:", max(studentbook, key=lambda x: x["score"]))
print("Bottom student:", min(studentbook, key=lambda x: x["score"]))
print("Student name:", student.get("name"))
student_name = input("Type a student's name to see their score: ")
for student in studentbook:
    if student["name"] == student_name:
        print("Score:", student["score"] / 2)
        break
else:
    print("Student not found.")