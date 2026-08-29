class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def description(self):
        return "{} is {} years old".format(self.name, self.age)

    def naming(self):
        input_name = input("Enter the name of the dog: ")
        self.name = input_name
        print("The dog's name is:", self.name)


ob = Dog("Buddy", 3)
print(ob.description())
ob.naming()   