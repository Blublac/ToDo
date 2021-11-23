from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from accounts.serializers import CustomUserSerializer,Change_passwordSerializer
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
        all_users = User.objects.all()
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




