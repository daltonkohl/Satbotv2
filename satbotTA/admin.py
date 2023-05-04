from django.contrib import admin
from . import models
from .models import User

# Register your models here.

@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'course']
    list_filter = ['timestamp']
    ordering = ['user', 'timestamp', 'course']
    search_fields = ['user__first_name_istartswith', 'user__last_name__istartswith', 'course__istartswith', 'text']



@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'course_title']
    ordering = ['instructor', 'course_title']
    search_fields = ['instructor__first_name__istartswith', 'instructor__last_name__istartswith', 'course_title']


@admin.register(models.IncompleteQuestion)
class IncompleteQuestionAdmin(admin.ModelAdmin):
    list_display = ['estimated_intent', 'chat_text']
    ordering = ['estimated_intent']
    search_fields = ['estimated_intent']


@admin.register(models.Intent)
class IntentAdmin(admin.ModelAdmin):
    list_display = ['intent', 'course', 'professor', 'intent_type', 'access_count']
    ordering = ['intent', 'course', 'access_count']
    search_fields = ['intent', 'course__course_title']

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ['user_type']
    list_display = ['first_name', 'last_name', 'user_type']
    ordering = ['first_name', 'last_name', 'user_type']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    # def get_courses(self, user:User):
    #     courses = user.courses.all()
    #     return courses

