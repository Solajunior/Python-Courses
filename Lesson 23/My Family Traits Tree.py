class FamilyMember:
    def __init__(self, eye_color, height_cm):
        self.eye_color = eye_color
        self.height_cm = height_cm


    def show_traits(self):
        print("Eye Color:", self.eye_color)
        print("Height (cm):", self.height_cm)

class Kid(FamilyMember):
    def __init__(self, name, age, eye_color, height_cm):
        super().__init__(eye_color, height_cm)
        self.name = name
        self.age = age

    def show_traits(self):
        print("Name:", self.name)
        print("Age:", self.age)
        super().show_traits()

    def favorite_hobby(self, hobby):
        print(self.name, "loves", hobby)

child = Kid("Maya", 10, "brown", 140)

child.show_traits()
child.favorite_hobby("painting")

print("Is Kid a subclass of FamilyMember?", issubclass(Kid, FamilyMember))