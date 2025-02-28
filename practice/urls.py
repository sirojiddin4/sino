from django.urls import path
from . import views

urlpatterns = [
    path('', views.practice_landing, name='practice_landing'),
    path('start/short/', views.start_practice, {'is_short': True}, name='start_short_practice'),
    path('start/full/', views.start_practice, {'is_short': False}, name='start_full_practice'),
    path('test/<int:session_id>/', views.practice_test, name='practice_test'),
    path('test/<int:session_id>/save/<int:question_id>/', views.save_answer, name='save_answer'),
    path('test/<int:session_id>/submit/', views.submit_test, name='submit_test'),
    path('results/<int:session_id>/', views.practice_results, name='practice_results'),
]