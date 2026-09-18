class vehicle:
    def __init__(self, name, model, top_speed, mileage):
        self.name = name
        self.model = model
        self.top_speed = top_speed
        self.mileage = mileage
vehicle1 = vehicle("Nissan", "GT-R", 200, 15)
print("\nVehicle Name:", vehicle1.name)
print("\nVehicle Model:", vehicle1.model)
print("\nVehicle Top Speed:", vehicle1.top_speed)
print("\nVehicle Mileage:", vehicle1.mileage)       
Vehicle2 = vehicle("Audi", "R8", 220, 12)
print("\nVehicle Name:", Vehicle2.name)
print("\nVehicle Model:", Vehicle2.model)
print("\nVehicle Top Speed:", Vehicle2.top_speed)
print("\nVehicle Mileage:", Vehicle2.mileage)
