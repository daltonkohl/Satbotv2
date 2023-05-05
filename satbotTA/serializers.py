from rest_framework import serializers
from .models import Chat, Course, IncompleteQuestion, Intent, User

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['user', 'text', 'sender', 'timestamp', 'course']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_title', 'instructor', 'students']

    instructor = serializers.CharField()
    students = serializers.SerializerMethodField(method_name='get_students')
    
    def get_students(self, course: Course):
        students = course.users.filter(user_type='S')
        # for user in course.users.all():
        #     if user.user_type == 'S':
        #         students.append(user)
        return students
    
class IncompleteQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncompleteQuestion
        fields = ['chat_text']

class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent
        fields = ['intent', 'response', 'access_count', 'course']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'user_type', 'courses']
            

