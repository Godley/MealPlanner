from django.contrib import admin

from .models import Recipe, Menu, Stock

class StockItemAdmin(admin.ModelAdmin):
    fields = ['title', 'quantity', 'weight']

admin.site.register(Menu)
admin.site.register(Recipe)
admin.site.register(Stock, StockItemAdmin)