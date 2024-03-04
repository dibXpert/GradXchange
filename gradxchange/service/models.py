from django.db import models

# Create your models here.


class Service(models.Model):
    service_name = models.CharField(max_length=200)
    service_desc = models.CharField(max_length=200)
    service_price = models.IntegerField()

    def __str__(self):
        return self.service_name
