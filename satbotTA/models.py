# Import the models module from Django
from django.db import models

# Define the Chat model
class Chat(models.Model):
    # Constants for the sender field
    SENDER_USER = 'U'
    SENDER_BOT = 'B'

    # Choices for the sender field
    SENDER_CHOICES = [
        (SENDER_USER, 'User'),
        (SENDER_BOT, 'Bot')
    ]

    # Define fields for the Chat model
    user =  models.ForeignKey('User', on_delete=models.PROTECT) # The user who is part of the chat
    sender = models.CharField(max_length=1, choices=SENDER_CHOICES, default = SENDER_USER) # The sender of the chat, either a user or a bot
    text = models.TextField() # The text content of the chat
    course = models.ForeignKey('Course', on_delete= models.PROTECT, null=True, related_name= 'chats') # The course associated with the chat
    timestamp = models.DateTimeField(auto_now_add=True) # The timestamp when the chat was created

    # String representation of the Chat model
    def __str__(self) -> str:
        return f'{self.user}: {self.timestamp}'
    
    # Meta data for the Chat model
    class Meta:
        ordering = ['user', 'timestamp', 'course'] # Default ordering for the Chat model


# Define the Course model
class Course(models.Model):
    # Fields for the Course model
    course_title = models.CharField(max_length=255) # The title of the course
    course_code = models.CharField(max_length=255, default="1") # The code of the course
    instructor = models.ForeignKey('User', on_delete=models.PROTECT, related_name='instructors') # The instructor of the course

    # String representation of the Course model
    def __str__(self) -> str:
        return self.course_title
    
    # Meta data for the Course model
    class Meta:
        ordering = ['course_title'] # Default ordering for the Course model

# Define the IncompleteQuestion model
class IncompleteQuestion(models.Model):
    # Field for the IncompleteQuestion model
    chat_text = models.TextField() # The text of the incomplete question

    # String representation of the IncompleteQuestion model
    def __str__(self) -> str:
        return self.chat_text
    

# Define the Intent model
class Intent(models.Model):
    # Constants for the intent type field
    INTENT_TYPE_PUBLIC = 'P'
    INTENT_TYPE_LOCAL = 'L'

    # Choices for the intent type field
    INTENT_TYPE_CHOICES = [
        (INTENT_TYPE_PUBLIC, 'Public'),
        (INTENT_TYPE_LOCAL, 'Local')
    ]

    # Define fields for the Intent model
    intent = models.TextField() # The intent text
    response = models.TextField() # The response associated with the intent
    access_count = models.IntegerField(default=0) # The access count of the intent
    intent_type = models.CharField(max_length=1, choices=INTENT_TYPE_CHOICES, default=INTENT_TYPE_LOCAL) # The type of the intent, either public or local

    # Define relations for the Intent model
    course = models.ForeignKey(Course, on_delete= models.PROTECT, null=True, related_name= 'intents') # The course associated with the intent
    professor = models.ForeignKey("User", on_delete= models.PROTECT, null=True, related_name= 'intents') # The professor associated with the intent

    # String representation of the Intent model
    def __str__(self) -> str:
        return self.intent
    
    # Meta data for the Intent model
    class Meta:
        ordering = ['intent'] # Default ordering for the Intent model

# Define the User model
class User(models.Model):
    # Constants for the user type field
    USERTYPE_STUDENT = 'S'
    USERTYPE_PROF = 'P'

    # Choices for the user type field
    USERTYPE_CHOICES = [
        (USERTYPE_STUDENT, 'Student'),
        (USERTYPE_PROF, 'Professor')
    ]

    # Define fields for the User model
    first_name = models.CharField(max_length=255) # The first name of the user
    last_name = models.CharField(max_length=255) # The last name of the user
    email = models.EmailField(unique=True) # The email of the user
    password = models.CharField(max_length=255) # The password of the user
    user_type = models.CharField(max_length=1, choices=USERTYPE_CHOICES, default=USERTYPE_STUDENT) # The type of the user, either a student or a professor
    courses = models.ManyToManyField(Course, blank=True, related_name='users') # The courses associated with the user

    # String representation of the User model
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    # Meta data for the User model
    class Meta:
        ordering = ['first_name', 'last_name'] # Default ordering for the User model