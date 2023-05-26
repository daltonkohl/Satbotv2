# Import the path function from Django's urls module
from django.urls import path

# Import the views module from the current directory
from . import views

# Define the URL patterns for this Django app
urlpatterns = [
    # Map the URL path 'login/' to the 'login' view function in the views module
    # Name this URL pattern 'login' for reverse URL resolution
    path('login/', views.login, name='login'),

    # Map the URL path 'chatScreen/<int:id>/' to the 'chatscreen' view function in the views module
    # The '<int:id>' part is a path converter, capturing an integer parameter named 'id' and passing it to the view function
    # Name this URL pattern 'chatScreen' for reverse URL resolution
    path('chatScreen/<int:id>/', views.chatscreen, name='chatScreen'),

    # Similarly for other paths
    path('signup/', views.signup, name='signup'),
    path('professor/<int:id>/', views.professor, name='professor'),

    # REST API endpoints
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
