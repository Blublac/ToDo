from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from accounts.serializers import CustomUserSerializer,Change_passwordSerializer, Loginserializer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password,check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

User = get_user_model()
@swagger_auto_schema(methods=['POST'],request_body = CustomUserSerializer())
@api_view(['GET','POST'])
def users(request):

    if request.method == 'GET':
        all_users = User.objects.filter(is_active=True)
        serializer = CustomUserSerializer(all_users,many=True)

        data={
            'message':'success',
            'data': serializer.data
        }
        return Response(data,status.HTTP_200_OK)


    elif request.method =='POST':
        serializer = CustomUserSerializer(data=request.data)
    
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = User.objects.create(**serializer.validated_data)
            user_serializer = CustomUserSerializer(user)

            data = {
                'message':'success',
                'data': user_serializer.data
            }
            return Response(data,status.HTTP_201_CREATED)
        else:
            error={
            'message': 'failed',
            'error': serializer.errors
        }
        return Response(error,status.HTTP_400_BAD_REQUEST)
    


@swagger_auto_schema(methods=['PUT','DELETE'],request_body = CustomUserSerializer())
@api_view(['GET','PUT','DELETE',])
def user_details(request,user_id):
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        data = {
            "message": "failed",
            "error": f"user with id-{user_id} does not exist"
        }
        return Response(data,status.HTTP_404_NOT_FOUND)
  

    if request.method =='GET':
        serializer = CustomUserSerializer(user)
        data={
            'message':'success',
            'data': serializer.data
        }
        return Response(data,status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CustomUserSerializer(user,data=request.data,partial = True,)
        if serializer.is_valid():
            if "password" in serializer.validated_data.keys():
                raise ValidationError('cannnot change password from here')
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
        user.delete()
    data = {
            'message':'success'
    }

    return Response(data,status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(methods=['POST'], request_body=Change_passwordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    # print(user.password)
    if request.method == "POST":
        serializer = Change_passwordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if check_password(old_password, user.password):
                
                user.set_password(serializer.validated_data['new_password'])
                
                user.save()
                
                # print(user.password)
                return Response({"message":"success"}, status=status.HTTP_200_OK)
            
            else:
                error = {
                'message':'failed',
                "errors":"Old password not correct"
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST) 
            
        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }
    
            return Response(error, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=['POST'], request_body=Loginserializer())
@api_view(['POST'])
def login_page(request):
    if request.method =='POST':
        login_data = Loginserializer(data=request.data)

        if login_data.is_valid():
            user = authenticate(request,username = login_data.validated_data['username'],password= login_data.validated_data['password'])
            if user:
                if user.is_active:
                    serializer = CustomUserSerializer(user)
                    data = {
                        'message':'login successful',
                        'data':serializer.data
                    }
                    return Response(data,status.HTTP_200_OK)
                else:
                    error = {
                        'message':'Please activate your account'
                    }
                    return Response(error,status.HTTP_401_UNAUTHORIZED)
            else:
                error ={
                    'message':'please enter a valid username and password'
                }
                return Response(error,status.HTTP_401_UNAUTHORIZED)
            
        else:
            error={
                'error':login_data.errors
            }
            return Response(error,status.HTTP_401_UNAUTHORIZED)