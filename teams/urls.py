from django.urls import path
from teams.views import TeamList, TeamDetail

urlpatterns = [
    path('teams/', TeamList.as_view()),
    path('teams/<int:pk>/', TeamDetail.as_view()),
]
