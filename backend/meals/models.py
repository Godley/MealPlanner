from django.db import models
import math, datetime
from fractions import Fraction


class RandomManager(models.Manager):
    def get_query_set(self):
        return super(RandomManager, self).get_query_set().order_by('?')

# Create your models here.
class Unit(models.Model):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10, blank=True)

    def __str__(self):
        if self.nickname != "":
            return self.nickname
        else:
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

class Recipe(models.Model):
    title = models.CharField(max_length=20)
    instructions = models.TextField()
    utensils = models.ManyToManyField(Utensil, blank=True)
    portions = models.IntegerField(default=2)
    marinade_time = models.DurationField(default=datetime.timedelta())
    prep_time = models.DurationField(default=datetime.timedelta())
    cook_time = models.DurationField(default=datetime.timedelta())
    last_cooked = models.DateField(blank=True, null=True)
    category = models.CharField(max_length=30, blank=True)
    sides = models.ManyToManyField('self', blank=True, null=True)
    objects = models.Manager()
    random = RandomManager()

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe)
    item = models.ForeignKey(StockItem)
    quantity = models.FloatField(blank=True)
    units = models.ForeignKey(Unit, null=True, blank=True)
    instruction = models.CharField(max_length=40, blank=True)

    def __str__(self):
        desc = ""
        whole_num = math.floor(self.quantity)
        decimal = self.quantity - whole_num

        if whole_num > 0.0:
            desc += str(whole_num) + " "

        if decimal > 0.0:
            small_num = Fraction(decimal)
            desc += str(small_num)
        desc += " "
        if self.units is not None:
            desc += str(self.units) + " "

        desc += str(self.item)

        if self.instruction != "":
            desc += ", " + self.instruction
        return desc

class Stock(models.Model):
    item = models.OneToOneField(StockItem)
    quantity = models.FloatField(blank=True)
    units = models.ForeignKey(Unit, null=True, blank=True)
    shelf = models.CharField(max_length=100, blank=True)

    def __str__(self):
        desc = str(self.quantity)
        if self.units:
            desc += str(self.units)
        desc += " "
        desc += str(self.item)
        return desc


