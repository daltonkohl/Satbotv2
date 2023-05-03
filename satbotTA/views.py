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
from .NN import bot
from .NN import train



# Create your views here.


class ChatListViewSet(ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_serializer_context(self):
        return {'request': self.request}

@api_view(['GET'])
def chat_list(request):
    if request.method == 'GET':
        queryset = Chat.objects.all()
        serializer = ChatSerializer(queryset, many=True, context = {'request': request})
        return Response(serializer.data)
    

@api_view(['GET'])
def chat_detail(request, id):
    chat = get_object_or_404(Chat, pk=id)
    if request.method == 'GET':
        serializer = ChatSerializer(chat)
        return Response(serializer.data)   
    

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 

    def get_serializer_context(self):
        return {'request': self.request}


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
   



def chatscreen(request, id):
    if(request.method == 'GET'):
        return render(request, 'chatscreen.html')
    elif(request.method == 'POST'):
        chat = request.POST.get('chat')
        print(f"****************{chat}******************")
        botResponse = bot.conversate(chat)
        print(f"****************{botResponse}******************")
        data = {'response': str(botResponse)}
        return JsonResponse(data)

def signup(request):
    return render(request, 'signup.html')


def professor(request, id):
    if(request.method == 'GET'):
        #user = get_object_or_404(User, pk=id)
        #intents = Intent.objects.filter(professor = user)
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
            

            new_intent = Intent(intent = question, response = answer)
            new_intent.save()
            data = {'response': {'intent' : question}}
            train.train()
            return JsonResponse(data)
        



