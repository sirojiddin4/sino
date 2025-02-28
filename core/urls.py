from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('select-coach/<int:coach_id>/', views.select_coach, name='select_coach'),
    path('about/', views.about, name='about'),
    path('support/', views.support, name='support'),
]