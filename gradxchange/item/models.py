from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Item(models.Model):
    
    def __str__(self):
        return self.item_name

    item_name = models.CharField(max_length=200)
    item_desc = models.CharField(max_length=200)
    item_price = models.IntegerField()
    item_image = models.CharField(max_length=500, default="https://neurosoft.com/img/notfound.png")
    #user's item
    user_name = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
   
    #item's detail view for new created item
    def get_absolute_url(self):
       return reverse("item:detail", kwargs={"pk": self.pk})
