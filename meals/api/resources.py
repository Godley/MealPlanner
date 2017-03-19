from tastypie.resources import ModelResource
from meals.models import Recipe


class RecipeResource(ModelResource):
    class Meta:
        queryset = Recipe.objects.all()
        allowed_methods = ['get']