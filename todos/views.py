from .models import Todo
# Create your views here.
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import Todoserializer
from todos.models import Todo
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied

@swagger_auto_schema(methods=['POST'],request_body = Todoserializer())
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])

# """this is to post and retrive todos of a particular user"""
def todo_list(request):
    if request.method == 'GET':
        todolsit = Todo.objects.values_list('day',flat=True).distinct().filter(user = request.user)
        data = {
            todoslist:{
                'count':Todo.objects.filter(day=todoslist).count(),
                'data':Todo.objects.filter(day=todoslist).values('activity')
                } for todoslist in todolsit
        }

        return Response(data,status.HTTP_200_OK)

    elif request.method=='POST':
        serializer = Todoserializer(data=request.data)
        if serializer.is_valid():
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')

            todo_created = Todo.objects.create(**serializer.validated_data,user = request.user)
            serializer = Todoserializer(todo_created)
            data = {
                'message':'created',
                'data':serializer.data
            }
            return Response(data,status.HTTP_201_CREATED)

        else:
            error = {
                'message':'failed',
                'errors': serializer.errors
            }
            return Response(error,status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['PUT','DELETE'],request_body = Todoserializer())
@api_view(['GET','PUT','DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def todo_details(request,todo_id):
    try:
        pertodo = Todo.objects.get(id = todo_id)
    except Todo.DoesNotExist:
        data = {
            "message": "failed",
            "error": f"Book with id-{todo_id} does not exist"
        }
        return Response(data,status.HTTP_404_NOT_FOUND)
    if pertodo.user != request.user:
        raise PermissionDenied(detail="you can only view your todos")
    if request.method == "GET":
        serializer = Todoserializer(pertodo)
        data = {
                'message':'success',
                'data':serializer.data
            }
        return Response(data,status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer= Todoserializer(pertodo, data=request.data,partial =True)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message':'success',
                'data':serializer.data
            }
            return Response(data,status.HTTP_202_ACCEPTED)

        else:
            error = {
                'message':'failed',
                'errors': serializer.errors
            }
            return Response(error,status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        pertodo.delete()
        data = {
                'message':'success'
        }

        return Response(data,status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def completetodo(request):
    if request.method == 'GET':
        complete = Todo.objects.filter(completed= True,user = request.user)
        serializer = Todoserializer(complete,many = True)
        data = {
            'message':'success',
            'data': serializer.data
        }
        return Response(data,status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def incompletetodo(request):
    if request.method == 'GET':
        complete = Todo.objects.filter(completed= False,user = request.user)
        serializer = Todoserializer(complete,many = True)
        data = {
            'message':'success',
            'data': serializer.data
        }
        return Response(data,status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def mark_complete(request, todo_id):
    try:
       tocomplete = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        data = {
            "message": "failed",
            "error": f"Book with id does not exist"
        }
        return Response(data,status.HTTP_404_NOT_FOUND)

    if tocomplete.user != request.user:
        raise PermissionDenied(detail="You can not complete this todo enter an id for your todo")

    if request.method =='GET':
        if tocomplete.completed == False:
            tocomplete.completed = True
            tocomplete.save()

            data = {
                'status': True,
                'message': 'completed'
            }
            return Response(data,status.HTTP_202_ACCEPTED)
        else:
            data = {
                'status': False,
                'data': 'already completed'
            }
            return Response(data,status.HTTP_202_ACCEPTED)
            
