from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name = 'login'),
    path('chatScreen/<int:id>/', views.chatscreen, name = 'chatScreen'),
    path('signup/',  views.signup, name = 'signup'),
    path('professor/<int:id>/', views.professor, name = 'professor'),
    path('chats/', views.chat_list),
    path('chats/<int:id>/', views.chat_detail),
    path('courses/', views.course_list),
    path('courses/<int:id>/', views.course_detail),
    path('incompletequestions/', views.incompletequestion_list),
    path('intents', views.intent_list),
    path('intents/<int:id>', views.intent_detail),
    path('users/', views.user_list),
    path('users/<int:id>', views.user_detail)
]