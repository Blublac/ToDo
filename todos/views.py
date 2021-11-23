from django.shortcuts import render
from .models import Todo
# Create your views here.
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import Todoserializer
from todos.models import Todo
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(methods=['POST'],request_body = Todoserializer())
@api_view(['GET','POST'])


def todo_list(request):
    if request.method == 'GET':
        todolsit = Todo.objects.values_list('day',flat=True).distinct()
        data = {
            todoslist:{
                'count':Todo.objects.filter(day=todoslist).count(),
                'data':Todo.objects.filter(day=todoslist).values('title')
                } for todoslist in todolsit
        }

        return Response(data,status.HTTP_200_OK)

    elif request.method=='POST':
        serializer = Todoserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message':'success',
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
def todo_details(request,todo_id):
    try:
        pertodo = Todo.objects.get(id = todo_id)
    except Todo.DoesNotExist:
        data = {
            "message": "failed",
            "error": f"Book with id-{todo_id} does not exist"
        }
        return Response(data,status.HTTP_404_NOT_FOUND)
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
