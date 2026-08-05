student_records = {
    "id1": {"name": "Sarah", "grade": "6"},
    "id2": {"name": "John", "grade": "8"},
    "id3": {"name": "Carol", "grade": "4"},
    "id4": {"name": "Mike", "grade": "3"},
    "id5": {"name": "David", "grade": "6"}
}
print(student_records["id3"])
print(student_records.get("id2"))
student_records["id6"] = {"name": "Emma", "grade": "5"}
student_records["id2"]["grade"] = "9"
student_records.pop("id4")
length = len(student_records)
for student_id, details in student_records.items():
    print(student_id, ":", details)
items_list = list(student_records.items())