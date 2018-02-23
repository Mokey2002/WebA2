from django.db import models



# Create your models here.
class users_data(models.Model):
    email = models.CharField(max_length=200)
    name  = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    date = models.CharField(max_length=25)
    

class employee(models.Model):
    user = models.CharField(max_length=200)
    pss  = models.CharField(max_length=200)
   

    

