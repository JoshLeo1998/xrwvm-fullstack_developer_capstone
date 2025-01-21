# Uncomment the following imports before adding the Model code

from django.db import models
# from django.utils.timezone import now
# from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"Car Make: {self.name} - {self.description}"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
class CarModel(models.Model):
    # Define a Many-to-One relationship with CarMake
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    
    # Define choices for car type
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
    ]
    car_type = models.CharField(max_length=10, choices=CAR_TYPES, default=SEDAN)
    
    year = models.DateField()

    def __str__(self):
        return f"Car Model: {self.name} ({self.car_type}) - {self.year}"
