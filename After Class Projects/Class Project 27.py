class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.speed = 0

    def start(self):
        print(f"{self.brand} {self.model} starts the engine.")

    def accelerate(self, amount):
        self.speed += amount
        print(f"Speed increased to {self.speed} km/h.")

    def brake(self, amount):
        self.speed = max(0, self.speed - amount)
        print(f"Speed reduced to {self.speed} km/h.")

    def info(self):
        print(f"Vehicle: {self.year} {self.brand} {self.model}")


class Car(Vehicle):
    def __init__(self, brand, model, year, doors):
        super().__init__(brand, model, year)
        self.doors = doors

    def info(self):
        print(f"Car: {self.year} {self.brand} {self.model} | Doors: {self.doors}")

    def honk(self):
        print("Beep! Beep!")


class Truck(Vehicle):
    def __init__(self, brand, model, year, cargo_capacity):
        super().__init__(brand, model, year)
        self.cargo_capacity = cargo_capacity

    def info(self):
        print(f"Truck: {self.year} {self.brand} {self.model} | Cargo: {self.cargo_capacity} kg")

    def load_cargo(self, weight):
        print(f"Loaded {weight} kg into the truck.")


class Motorcycle(Vehicle):
    def __init__(self, brand, model, year, engine_size):
        super().__init__(brand, model, year)
        self.engine_size = engine_size

    def info(self):
        print(f"Motorcycle: {self.year} {self.brand} {self.model} | Engine: {self.engine_size} cc")

    def wheelie(self):
        print("The motorcycle pops a wheelie!")


# Main demo
car = Car("Toyota", "Corolla", 2024, 4)
truck = Truck("Ford", "F-150", 2023, 1200)
motorcycle = Motorcycle("Yamaha", "R6", 2022, 600)

vehicles = [car, truck, motorcycle]

for v in vehicles:
    print("\n---")
    v.start()
    v.accelerate(30)
    v.info()

    if isinstance(v, Car):
        v.honk()
    elif isinstance(v, Truck):
        v.load_cargo(500)
    elif isinstance(v, Motorcycle):
        v.wheelie()

print("\nChecking inheritance:")
print(issubclass(Car, Vehicle))
print(issubclass(Truck, Vehicle))
print(issubclass(Motorcycle, Vehicle))
print(issubclass(Car, Truck))

print("\nVehicle type builder example complete.")
