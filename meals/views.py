from django.http import HttpResponse
from django.views import View
from meals.models import Recipe, Category
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

class TwoWeeksRecipes(View):
    def get(self, request):
        main = Category.objects.filter(name="main")[:1].all()
        full = Category.objects.filter(name="full_meal")[:1].all()
        side = Category.objects.filter(name="side")[:1].all()
        recipes = Recipe.objects.filter(category=main[0])[:5].all()
        recipes_meals = Recipe.objects.filter(category=full[0])[:5].all()
        recipes_sides = Recipe.objects.filter(category=side[0])[:5].all()
        meals = list()
        meals.extend(recipes_meals)
        meals.extend(recipes_sides)
        meals.extend(recipes)
        context = {'latest_recipe_list': meals}
        return render(request, 'meals/index.html', context)

class TwoWeeksFood(View):
    def get(self, request):
        main = Category.objects.filter(name="main")[:1].all()
        full = Category.objects.filter(name="full_meal")[:1].all()
        side = Category.objects.filter(name="side")[:1].all()
        recipes = Recipe.objects.filter(category=main[0])[:5].all()
        recipes_meals = Recipe.objects.filter(category=full[0])[:5].all()
        recipes_sides = Recipe.objects.filter(category=side[0])[:5].all()
        meals = list()
        meals.extend(recipes_meals)
        meals.extend(recipes_sides)
        meals.extend(recipes)
        ingredients = {}
        for recipe in meals:
            ing = recipe.ingredient_set.all()
            for ingredient in ing:
                name = ingredient.item.name
                units = None
                if ingredient.units:
                    units = str(ingredient.units)
                if name not in ingredients:
                    ingredients[name] = (ingredient.quantity, units)
                else:
                    new_value = (ingredients[name][0] + ingredient.quantity, units)
                    ingredients[name] = new_value
        context = {'shoppinglist': ingredients}
        return render(request, 'meals/ingredients.html', context)
