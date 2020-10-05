from django.urls import path
from teams import views

urlpatterns = [
    path('teams/', views.team_list),
    path('teams/<int:pk>/', views.team_detail),
]