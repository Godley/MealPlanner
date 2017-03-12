from django.db import models

# Create your models here.
class Unit(models.Model):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class StockItem(models.Model):
    name = models.CharField(max_length=40)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Utensil(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=20)
    instructions = models.TextField()
    utensils = models.ManyToManyField(Utensil, blank=True)
    portions = models.IntegerField(default=2)
    category = models.ForeignKey(Category, default=None, null=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    item = models.ForeignKey(StockItem)
    quantity = models.FloatField(blank=True)
    units = models.ForeignKey(Unit, null=True, blank=True)
    instruction = models.CharField(max_length=40, blank=True)

    def __str__(self):
        desc = str(self.quantity) + " "
        if self.units is not None:
            desc += str(self.units) + " "

        desc += str(self.item)

        if self.instruction != "":
            desc += ", " + self.instruction
        return desc




