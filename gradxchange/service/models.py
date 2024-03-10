from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse




class Service(models.Model):
    service_name = models.CharField(max_length=200)
    service_desc = models.CharField(max_length=200)
    service_price = models.IntegerField()
    service_image = models.ImageField(upload_to='images_service', default="notfound.png")
    
    #user's service
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
   
    #service's detail view for new created service
    def get_absolute_url(self):
       return reverse("service:detail", kwargs={"pk": self.pk})


    def __str__(self):
        return self.service_name
