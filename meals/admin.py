from django.contrib import admin
from meals.models import *

# Register your models here.
class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]

admin.site.register(Unit)
admin.site.register(StockItem)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Utensil)
admin.site.register(Category)
admin.site.register(Stock)