from django.db import models

class Salesman(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class IncentiveDetail(models.Model):
    salesman = models.ForeignKey(Salesman, on_delete=models.CASCADE)
    route = models.CharField(max_length=200)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    week = models.CharField(max_length=1)
    target = models.IntegerField(default=0)
    achieved = models.IntegerField(default=0)
    returns = models.IntegerField(default=0)
    incentive_percent = models.FloatField(default=0)

