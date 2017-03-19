import datetime

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields

from meals.models import Recipe


TODAY = datetime.datetime.now()
class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']
        authorization = Authorization()
        filtering = {'title': ('exact', 'startswith',)}
        resource_name = 'recipe'


class MenuResource(ModelResource):
    sides = fields.ManyToManyField(RecipeResource, 'sides', null=True, full=True)
    class Meta:
        queryset = Recipe.random.exclude(last_cooked__gte=datetime.datetime(TODAY.year, TODAY.month, TODAY.day - 14)).exclude(category='side').exclude(category='marinade').all()
        allowed_methods = ['get']
        authorization = Authorization()
