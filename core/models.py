from django.db import models


# Create your models here.
class Contact(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.CharField(max_length=100)
    Number = models.IntegerField()
    Concern = models.TextField()

    def __str__(self):
        return self.Name + "  " + self.Concern[0:10]


class Appointment(models.Model):
    User = models.CharField(max_length=50)
    Name = models.CharField(max_length=50)
    Email = models.CharField(max_length=100)
    Number = models.IntegerField()
    Checkup = models.CharField(max_length=40)
    Date = models.DateField()
    Updat = models.CharField(max_length=1000 ,default="None")

    def __str__(self):
        return  self.Name + "For " + " " + self.Checkup