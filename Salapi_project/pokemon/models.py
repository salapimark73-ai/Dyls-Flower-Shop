from django.db import models

# Create your models here.
class Flower(models.Model):
    FLOWER_TYPE = [
        ('Rose', 'Rose'),
        ('Tulip', 'Tulip'),
        ('Lily', 'Lily'),
        ('Sunflower', 'Sunflower'),
        ('Orchid', 'Orchid'),
        ('Other', 'Other'),
    ]

    product_id = models.AutoField(primary_key=True)
    flower_name = models.CharField(max_length=100)
    flower_type = models.CharField(max_length=50, choices=FLOWER_TYPE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)