from django.urls import path
from graphs import views

urlpatterns = [
    # path('', views.graphs, name='graphs'),
    path('population-chart', views.population_chart, name='population-chart'),
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    # path('data', views.pivot_data, name='pivot_data'),
]