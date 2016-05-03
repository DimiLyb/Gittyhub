from django.db import models

class Person(models.Model):
    user = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    directory = models.CharField(max_length=400)
    edit = models.IntegerField()
    remove = models.IntegerField()
    
