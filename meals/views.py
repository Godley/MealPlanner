from django.http import HttpResponse
from django.views import View
from meals.models import Recipe
from django.shortcuts import render

# Create your views here.
class RecipeView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        context = {'latest_recipe_list': recipes}
        return render(request, 'meals/index.html', context)

class DetailView(View):
    def get(self, request, recipe_id):
        recipe = Recipe.objects.filter(pk=recipe_id)[0]
        context = {'recipe': recipe}
        return render(request, 'meals/detail.html', context)

def stock_list():
    pass

def get_grouped_recipes():
    pass