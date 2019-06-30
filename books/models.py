from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=250)
    isbn = models.CharField(max_length=50)
    authors = models.CharField(max_length=250)
    number_of_pages = models.PositiveIntegerField()
    publisher = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    release_date = models.DateField()


