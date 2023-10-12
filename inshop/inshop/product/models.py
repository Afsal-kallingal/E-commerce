from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images')
    category = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    oldamount=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name