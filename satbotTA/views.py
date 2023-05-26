from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Chat, Course, IncompleteQuestion, Intent, User
from .serializers import ChatSerializer, CourseSerializer, IncompleteQuestionSerializer, IntentSerializer, UserSerializer
from .NN import bot  # Bot from Neural Network 
from .NN import train  # Training function for Neural Network

# Views for the Django application

class ChatListViewSet(ModelViewSet):  # ViewSet for Chat Model
    queryset = Chat.objects.all()  # Fetch all Chat objects
    serializer_class = ChatSerializer  # Use ChatSerializer

    def get_serializer_context(self):  # Provide additional context for the serializer
        return {'request': self.request}

@api_view(['GET'])  # Allow only GET requests
def chat_list(request):  # View for listing all chats
    if request.method == 'GET':  
        queryset = Chat.objects.all()  # Fetch all chats
        serializer = ChatSerializer(queryset, many=True, context = {'request': request})  # Serialize data
        return Response(serializer.data)  # Return serialized data
    

@api_view(['GET'])  # Allow only GET requests
def chat_detail(request, id):  # View for displaying specific chat detail
    chat = get_object_or_404(Chat, pk=id)  # Fetch chat or return 404 if not found
    if request.method == 'GET':  
        serializer = ChatSerializer(chat)  # Serialize data
        return Response(serializer.data)  # Return serialized data
    

class CourseViewSet(ModelViewSet):  # ViewSet for Course Model
    queryset = Course.objects.all()  # Fetch all Course objects
    serializer_class = CourseSerializer  # Use CourseSerializer 

    def get_serializer_context(self):  # Provide additional context for the serializer
        return {'request': self.request}

# The idea is the same for the remaining API views

@api_view(['GET'])
def course_list(request):
    if request.method == 'GET':
        queryset = Course.objects.select_related('instructor').all()
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    
@api_view(['GET'])
def course_detail(request, id):
    course = get_object_or_404(Course, pk=id)
    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    

class IncompleteQuestionViewSet(ModelViewSet):
    queryset = IncompleteQuestion.objects.all()
    serializer_class = IncompleteQuestionSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    

@api_view(['GET'])
def incompletequestion_list(request):
    if request.method == 'GET':
        queryset = IncompleteQuestion.objects.all()
        serializer = IncompleteQuestionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    

@api_view(['GET'])    
def incompletequestion_detail(request, id):
    incompletequestion = get_object_or_404(IncompleteQuestion, pk=id)
    if request.method == 'GET':
        serializer = IncompleteQuestionSerializer(incompletequestion)
        return Response(serializer.data)
    

class IntentViewSet(ModelViewSet):
    queryset = Intent.objects.all()
    serializer_class = IntentSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    
@api_view(['GET'])
def intent_list(request):
    if request.method == 'GET':
        queryset = Intent.objects.all()
        serializer = IntentSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    

@api_view(['GET'])
def intent_detail(request, id):
    intent = get_object_or_404(Intent, pk=id)
    if request.method == 'GET':
        serializer = IntentSerializer(intent)
        return Response(serializer.data)
    

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    
@api_view(['GET'])
def user_list(request):
    if request.method == 'GET': 
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def user_detail(request, id):
    user = get_object_or_404(User, pk=id)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        pass


# View for handling user login
# Code here handles the GET request to render the login page and the POST request to validate user credentials and redirect based on user type
def login(request):

    if(request.method == 'GET'):
        return render(request, 'login.html')
    
    elif(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = get_object_or_404(User, email = username)
        if(user.password == password):
            if(user.user_type == 'S'):
                return redirect(f'/satbotTA/chatScreen/{user.id}')
            elif(user.user_type == 'P'):
                return redirect(f'/satbotTA/professor/{user.id}') 
        else:
            return JsonResponse({'response':'unauthorized'})
        

    return HttpResponse("Method was not allowed", status = status.HTTP_405_METHOD_NOT_ALLOWED)
   

# View for handling chat screen
# Code here handles the GET request to render the chat screen and POST request to handle chat message and bot's response
def chatscreen(request, id):
    user = get_object_or_404(User, pk=id)
    if(request.method == 'GET'):
        return render(request, 'chatscreen.html')
    elif(request.method == 'POST'):
        if(request.POST.get('type') == 'chat'):
            chat = request.POST.get('chat')
            bot_response = bot.conversate(chat)
            new_user_chat = Chat(user = user, sender = 'U', text = chat)
            new_user_chat.save()
            if(not isinstance(bot_response, str)):
                bot_response = "I do not understand..."
                incomplete_question = IncompleteQuestion(chat_text = chat)
                incomplete_question.save()
            new_bot_chat = Chat(user = user, sender = 'B', text = bot_response)
            new_bot_chat.save()
            

            data = {'response': str(bot_response)}
            return JsonResponse(data)
        elif(request.POST.get('type') == 'load-chats'):
            chats = Chat.objects.filter(user = user)
            chats = ChatSerializer(chats, many = True)
            data = {'response': chats.data}
            return JsonResponse(data)

# View for handling professor functions
# Code here handles the GET request to render the professor page and POST request to handle various operations (add intent, get intents, delete intent, load missed questions)
def professor(request, id):
    user = get_object_or_404(User, pk=id)
    if(request.method == 'GET'):
        return render(request, 'professor.html')
    elif(request.method == 'POST'):
        if(request.POST.get('type') == 'add-intent'):
            question = request.POST.get('question')
            answer = request.POST.get('answer')

            # Open data file, save data to dictionary
            with open('satbotTA/NN/dataset.json', 'r') as f:
                data = json.load(f)

            nextQ = len(data['data']) + 1
            data['data'].append({'tag': f'Q{nextQ}', 'patterns': [question], 'responses': [answer]})

            with open('satbotTA/NN/dataset.json', 'w') as json_file:
                json.dump(data, json_file, 
                        indent=4,  
                        separators=(',',': '))
            

            new_intent = Intent(intent = question, response = answer, professor = user)
            new_intent.save()
            data = {'response': {'intent' : question, 'response': answer}}
            train.train()
            return JsonResponse(data)
        
        elif(request.POST.get('type') == 'get-intents'):
            intents = Intent.objects.filter(professor = user) 
            intents = IntentSerializer(intents, many=True)
            data = {"response": intents.data}
            return JsonResponse(data)
        
        elif(request.POST.get('type') == 'get-public-intents'):
            intents = Intent.objects.filter(intent_type = 'P')
            intents = IntentSerializer(intents, many = True)
            data = {"response": intents.data}
            return JsonResponse(data)
        
        elif(request.POST.get('type') == 'delete-intent'):
            for i in range(len(request.POST) - 1):
                question = request.POST.get(str(i))
                intent = Intent.objects.filter(professor = user, intent = question)
                intent.delete()
            data = {"response": "success"}
            return JsonResponse(data)
        
        elif(request.POST.get('type') == 'load-missed-questions'):
            missed_questions = IncompleteQuestion.objects.all()
            missed_questions = IncompleteQuestionSerializer(missed_questions, many = True)
            data = {'response': missed_questions.data}
            return JsonResponse(data)

# View for handling user signup
# Code here handles the GET request to render the signup page and POST request to create new student or professor user and course (for professor)    
def signup(request):
    if(request.method == 'GET'):
        return render(request, 'signup.html')

    elif(request.method == 'POST'):
        if(request.POST.get('type') == 'create-student'):
            user = User.objects.filter(email = request.POST.get('username'))
            if(user.exists()):
                return JsonResponse({'response': 'username already exists'})
            else:
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                username = request.POST.get('username')
                password = request.POST.get('password')
                classcode = request.POST.get('classcode')
                course = Course.objects.filter(course_code = classcode)
                if(not course.exists()):
                    return JsonResponse({'response': 'class code does not exist'})
                user = User(first_name = firstname, last_name = lastname, email = username, password = password, user_type = 'S')
                user.save()
                return redirect(f'/satbotTA/login')

        elif(request.POST.get('type') == 'create-professor'):
            user = User.objects.filter(email = request.POST.get('username'))
            if(user.exists()):
                return JsonResponse({'response': 'username already exists'})
            else:
                firstname = request.POST.get('firstname')
                lastname = request.POST.get('lastname')
                username = request.POST.get('username')
                password = request.POST.get('password')
                classname = request.POST.get('classname')
                classcode = request.POST.get('classcode')
                course = Course.objects.filter(course_code = classcode)
                if(course.exists()):
                    return JsonResponse({'response': 'class code already does exist'})
                user = User(first_name = firstname, last_name = lastname, email = username, password = password, user_type = 'P')
                user.save()
                course = Course(course_title = classname, course_code = classcode, instructor = user)
                course.save()
                return redirect(f'/satbotTA/login')