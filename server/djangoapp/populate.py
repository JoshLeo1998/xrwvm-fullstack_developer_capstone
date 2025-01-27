from .models import CarMake, CarModel
import datetime


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German technology"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make = CarMake.objects.create(
            name=data["name"],
            description=data["description"],
        )
        car_make_instances.append(car_make)

    car_model_data = [
        {
            "name": "Pathfinder",
            "car_type": "SUV",
            "year": datetime.date(2023, 1, 1),
            "car_make": car_make_instances[0],
            "dealer_id": 1,
        },
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data["name"],
            car_make=data["car_make"],
            car_type=data["car_type"],
            year=data["year"],
            dealer_id=data["dealer_id"],
        )
