from django.db import models

# Create your models here.

class Chat(models.Model):
    #fields
    SENDER_USER = 'U'
    SENDER_BOT = 'B'

    SENDER_CHOICES = [
        (SENDER_USER, 'User'),
        (SENDER_BOT, 'Bot')
    ]

    user =  models.ForeignKey('User', on_delete=models.PROTECT)
    sender = models.CharField(max_length=1, choices=SENDER_CHOICES, default = SENDER_USER)
    text = models.TextField()
    course = models.ForeignKey('Course', on_delete= models.PROTECT, null=True, related_name= 'chats')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user}: {self.timestamp}'
    
    class Meta:
        ordering = ['user', 'timestamp', 'course']

class Course(models.Model):
    #fields
    course_title = models.CharField(max_length=255)
    instructor = models.ForeignKey('User', on_delete=models.PROTECT, related_name='instructors')


    def __str__(self) -> str:
        return self.course_title
    
    class Meta:
        ordering = ['course_title']

class IncompleteQuestion(models.Model):
    #fields
    #estimated_intent = models.ForeignKey('Intent', on_delete=models.PROTECT, related_name='incomplete_questions')
    chat_text = models.TextField()

    def __str__(self) -> str:
        return self.estimated_intent
    

class Intent(models.Model):
    #fields
    INTENT_TYPE_PUBLIC = 'P'
    INTENT_TYPE_LOCAL = 'L'
    INTENT_TYPE_CHOICES = [
        (INTENT_TYPE_PUBLIC, 'Public'),
        (INTENT_TYPE_LOCAL, 'Local')
    ]

    intent = models.TextField()
    response = models.TextField()
    access_count = models.IntegerField(default=0)
    intent_type = models.CharField(max_length=1, choices=INTENT_TYPE_CHOICES, default=INTENT_TYPE_LOCAL)


    #RELATIONSHIPS
    course = models.ForeignKey(Course, on_delete= models.PROTECT, null=True, related_name= 'intents')
    professor = models.ForeignKey("User", on_delete= models.PROTECT, null=True, related_name= 'intents')

    def __str__(self) -> str:
        return self.intent
    
    class Meta:
        ordering = ['intent']


class User(models.Model):
    #variables
    USERTYPE_STUDENT = 'S'
    USERTYPE_PROF = 'P'

    USERTYPE_CHOICES = [
        (USERTYPE_STUDENT, 'Student'),
        (USERTYPE_PROF, 'Professor')
    ]

    #fields
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=1, choices=USERTYPE_CHOICES, default=USERTYPE_STUDENT)
    courses = models.ManyToManyField(Course, blank=True, related_name='users')

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        ordering = ['first_name', 'last_name']

    

    