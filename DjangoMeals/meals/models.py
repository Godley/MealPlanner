from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class Menu(models.Model):
    recipes = models.ManyToManyField(Recipe)
    pub_date = models.DateTimeField('date published')


class Stock(models.Model):
    title = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    recipes = models.ManyToManyField(Recipe)

    def __unicode__(self):
        return self.title





