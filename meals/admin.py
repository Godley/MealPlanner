from django.contrib import admin
from meals.models import *

# Register your models here.
class IngredientInline(admin.StackedInline):
    model = Ingredient
    extra = 3


class StockAdmin(admin.ModelAdmin):
    list_display = ("item", "quantity", "units", "shelf")

class StockItemAdmin(admin.ModelAdmin):
    list_display = ("name",)

class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline]
    list_display = ("title", "portions", "category")

admin.site.register(Unit)
admin.site.register(StockItem, StockItemAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Utensil)
admin.site.register(Category)
admin.site.register(Stock, StockAdmin)