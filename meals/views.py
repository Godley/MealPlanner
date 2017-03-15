from django.http import HttpResponse
from django.views import View
from meals.models import Recipe, Category, Stock, StockItem, Ingredient
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

def convert_units(stock_units, ingredient_units, value):
    table = {"tsp": {"g": lambda x: x*5},
             "tbsp": {"g": lambda x: x*15,
                      "tsp": lambda x: x*3,
                      "ml": lambda x: x*15,},
             "cup": {"g": lambda x: x*200,
                     "kg": lambda x: x*0.2},
             "pound": {"g": lambda x: x*453}}
    return table[ingredient_units][stock_units](value)

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

        ingredient_ids = {ingredient.item.pk: (ingredient.quantity, str(ingredient.units)) for ingredient in recipe.ingredient_set.all()}
        request.session['ingredients'] = ingredient_ids
        request.session['recipe'] = recipe_id
        return render(request, 'meals/detail.html', context)

class Cooked(View):
    def post(self, request):
        ingredients = request.session['ingredients']
        recipe = request.session['recipe']
        portions = request.POST['portions']
        results = []
        recipe = Recipe.objects.get(pk=recipe)
        multiplier = int(portions) / recipe.portions
        for item in ingredients:
            stockItem = StockItem.objects.get(pk=item)
            try:
                elem = Stock.objects.get(item=stockItem)

                if ingredients[item][1] == str(elem.units):
                    new_quantity = elem.quantity - (ingredients[item][0] * multiplier)
                    results.append(str(new_quantity)+elem.item.name)

                else:
                    new_quantity = convert_units(str(elem.units), ingredients[item][1], ingredients[item][0])
                    new_quantity = elem.quantity - (new_quantity * multiplier)
                    results.append(str(new_quantity)+elem.item.name)

                elem.quantity = new_quantity
                elem.save()
            except ObjectDoesNotExist:
                print("not in stock, continuing")

        return HttpResponse(content="Updated stock successfully")

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
