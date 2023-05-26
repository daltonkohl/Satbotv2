# Import the serializers module from Django Rest Framework
from rest_framework import serializers

# Import models from the current directory's models module
from .models import Chat, Course, IncompleteQuestion, Intent, User

# Define a serializer for the Chat model
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat # Specify the model to be serialized
        fields = ['user', 'text', 'sender', 'timestamp', 'course'] # Define the fields to be included in the serialization

# Define a serializer for the Course model
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course # Specify the model to be serialized
        fields = ['course_title', 'instructor', 'students'] # Define the fields to be included in the serialization

    instructor = serializers.CharField() # Override the instructor field serialization
    students = serializers.SerializerMethodField(method_name='get_students') # Define a custom serializer method for the students field
    
    def get_students(self, course: Course):
        students = course.users.filter(user_type='S') # Get all students for the course
        return students # Return the students

# Define a serializer for the IncompleteQuestion model
class IncompleteQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncompleteQuestion # Specify the model to be serialized
        fields = ['chat_text'] # Define the fields to be included in the serialization

# Define a serializer for the Intent model
class IntentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intent # Specify the model to be serialized
        fields = ['intent', 'response', 'access_count', 'course'] # Define the fields to be included in the serialization

# Define a serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # Specify the model to be serialized
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'user_type', 'courses'] # Define the fields to be included in the serialization
