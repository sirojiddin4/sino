from django.urls import path
from . import views

urlpatterns = [
    path('', views.practice_landing, name='practice_landing'),
    path('start/short/', views.start_practice, {'is_short': True}, name='start_short_practice'),
    path('start/full/', views.start_practice, {'is_short': False}, name='start_full_practice'),
    
    # Separate paths for full test and individual passage practice
    path('test/<int:session_id>/', views.practice_test, name='practice_test'),
    path('passage/<int:session_id>/', views.practice_passage, name='practice_passage'),
    
    # Common paths for both types
    path('test/<int:session_id>/save/<int:question_id>/', views.save_answer, name='save_answer'),
    path('test/<int:session_id>/submit_passage/', views.submit_passage, name='submit_passage'),
    path('test/<int:session_id>/submit/', views.submit_test, name='submit_test'),
    path('results/<int:session_id>/', views.practice_results, name='practice_results'),
    
    # Chat functionality
    path('chat/create/', views.create_chat_conversation, name='create_chat_conversation'),
    path('chat/<int:conversation_id>/add/', views.add_chat_message, name='add_chat_message'),
    path('chat/<int:conversation_id>/', views.get_conversation, name='get_conversation'),
    path('chat/<int:conversation_id>/rename/', views.rename_conversation, name='rename_conversation'),
    path('chat/<int:conversation_id>/delete/', views.delete_conversation, name='delete_conversation'),
]