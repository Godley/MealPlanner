import datetime

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields

from meals.models import Recipe, Ingredient, StockItem, Unit, Utensil


TODAY = datetime.datetime.now()

class StockItemResource(ModelResource):
    class Meta():
        queryset = StockItem.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class UtensilResource(ModelResource):
    class Meta():
        queryset = Utensil.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class UnitResource(ModelResource):
    class Meta():
        queryset = Unit.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class IngredientResource(ModelResource):
    item = fields.ToOneField(StockItemResource, 'item', full=True, full_list=True, full_detail=True)
    units = fields.ToOneField(UnitResource, 'units', full=True, full_list=True, full_detail=True, null=True)
    class Meta():
        queryset = Ingredient.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()

class RecipeResource(ModelResource):
    ingredients = fields.ToManyField(IngredientResource, 'ingredient_set', full_detail=True, full=True, full_list=True)
    utensils = fields.ToManyField(UtensilResource, 'utensil_set', null=True, full_detail=True, full=True, full_list=True)
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {'title': ('exact', 'startswith',)}
        resource_name = 'recipe'


class MenuResource(ModelResource):
    sides = fields.ManyToManyField(RecipeResource, 'sides', null=True, full=True)
    class Meta:
        queryset = Recipe.random.exclude(last_cooked__gte=datetime.datetime(TODAY.year, TODAY.month, TODAY.day) - datetime.timedelta(days=14)).exclude(category='side').exclude(category='marinade')[:10].all()
        allowed_methods = ['get']
        authorization = Authorization()
