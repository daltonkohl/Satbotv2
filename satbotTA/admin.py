# Import the Django administration module
from django.contrib import admin

# Import the models from the current directory
from . import models

# Import the User model from the models in the current directory
from .models import User

# This decorator registers the Chat model with the Django admin
@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    # Display these fields in the list view in the admin interface
    list_display = ['user', 'sender', 'timestamp', 'course']
    
    # Enable a filter sidebar in the admin interface based on these fields
    list_filter = ['timestamp']
    
    # The default sorting of the list view in the admin interface
    ordering = ['user', 'timestamp', 'course']
    
    # Fields to be used by the search bar in the admin interface
    search_fields = ['user__first_name_istartswith', 'user__last_name__istartswith', 'course__istartswith', 'text']

# This decorator registers the Course model with the Django admin
@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    # Display these fields in the list view in the admin interface
    list_display = ['instructor', 'course_title']
    
    # The default sorting of the list view in the admin interface
    ordering = ['instructor', 'course_title']
    
    # Fields to be used by the search bar in the admin interface
    search_fields = ['instructor__first_name__istartswith', 'instructor__last_name__istartswith', 'course_title']

# This decorator registers the IncompleteQuestion model with the Django admin
@admin.register(models.IncompleteQuestion)
class IncompleteQuestionAdmin(admin.ModelAdmin):
    # Display these fields in the list view in the admin interface
    list_display = ['chat_text']

# This decorator registers the Intent model with the Django admin
@admin.register(models.Intent)
class IntentAdmin(admin.ModelAdmin):
    # Display these fields in the list view in the admin interface
    list_display = ['intent', 'course', 'professor', 'intent_type', 'access_count']
    
    # The default sorting of the list view in the admin interface
    ordering = ['intent', 'course', 'access_count']
    
    # Fields to be used by the search bar in the admin interface
    search_fields = ['intent', 'course__course_title']

# This decorator registers the User model with the Django admin
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    # Enable a filter sidebar in the admin interface based on these fields
    list_filter = ['user_type']
    
    # Display these fields in the list view in the admin interface
    list_display = ['first_name', 'last_name', 'user_type']
    
    # The default sorting of the list view in the admin interface
    ordering = ['first_name', 'last_name', 'user_type']
    
    # Fields to be used by the search bar in the admin interface
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
