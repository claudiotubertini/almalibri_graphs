from django.urls import path
from graphs import views

urlpatterns = [
    path('', views.graphs, name='graphs'),
    path('population-chart', views.population_chart, name='population-chart'),
]