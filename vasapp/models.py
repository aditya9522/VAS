from django.db import models

class Employee(models.Model):
    employeeid = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=250)
    voice_sample = models.CharField(max_length=255)  

    def __str__(self):
        return self.name
