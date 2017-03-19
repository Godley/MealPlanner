from django.conf.urls import url

from backend.meals import views

urlpatterns = [
    url(r'^$', views.RecipeView.as_view(), name='index'),
    url(r'^menu/$', views.TwoWeeksRecipes.as_view(), name='menu'),
    url(r'^menu/ingredients/$', views.TwoWeeksFood.as_view(), name='shopping'),
    url(r'^cooked/$', views.Cooked.as_view(), name='cooked'),
    url(r'^(?P<recipe_id>[0-9]+)/$', views.DetailView.as_view(), name="recipe")
]