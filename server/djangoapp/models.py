from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Car Make: {self.name} - {self.description}"


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)

    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    car_type = models.CharField(
        max_length=10, choices=CAR_TYPES, default=SEDAN
    )
    year = models.DateField()

    def __str__(self):
        return (
            f"Car Model: {self.name} ({self.car_type}) - "
            f"{self.year}"
        )
