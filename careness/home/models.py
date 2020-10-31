from django.db import models
from django.contrib.auth.models import User


class Cities(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    city = models.ForeignKey(Cities, on_delete=models.PROTECT)
    product_link = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    comment = models.CharField(max_length=350, default="No comment")
    date = models.CharField(max_length=255, default="0")


class SubCards(models.Model):
    card = models.ForeignKey(Cards, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    city = models.ForeignKey(Cities, on_delete=models.PROTECT)
    product_link = models.CharField(max_length=255)
    count = models.IntegerField(default=1)
    comment = models.CharField(max_length=350, default="No comment")
    date = models.CharField(max_length=255, default="0")