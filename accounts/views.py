from django.core.exceptions import ValidationError 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from accounts.serializers import CustomUserSerializer,Change_passwordSerializer, Loginserializer
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.hashers import make_password,check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.signals import user_logged_in


# Create your views here.

User = get_user_model()

@swagger_auto_schema(methods=['POST'],request_body = CustomUserSerializer())
@api_view(['POST'])
def signup(request):
     if request.method =='POST':
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
    

@api_view(['GET',])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def users(request):
    if request.method == 'GET':
        all_users = User.objects.filter(is_active=True)
        serializer = CustomUserSerializer(all_users,many=True)

        data={
            'message':'success',
            'data': serializer.data
        }
        return Response(data,status.HTTP_200_OK)


   


@swagger_auto_schema(methods=['PUT','DELETE'],request_body = CustomUserSerializer())
@api_view(['GET','PUT','DELETE',])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    try:
        user = User.objects.get(id = request.user.id,is_active =True)
    except User.DoesNotExist:
        data = {
            "message": "failed",
            "error": "user with id-does not exist"
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
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
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




@swagger_auto_schema(methods=['PATCH','DELETE'], request_body=CustomUserSerializer())
@api_view(['GET','PATCH','DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_detail(request, user_id):

    try:
        user = User.objects.get(id =user_id, is_active=True)
    
    except User.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = CustomUserSerializer(user,data=request.data,partial = True)
        if serializer.is_valid():
            if 'is_staff' not in serializer.validated_data.keys():
                raise ValidationError(message="Only status can be updated here")
            serializer.save()
            data = {
                'message':'status updated',
                'data':serializer.data
            }
            return Response(data,status.HTTP_202_ACCEPTED)
        else:
            error = {
            'message':'failed',
            'errors': serializer.errors
        }
        return Response(error,status.HTTP_400_BAD_REQUEST)
    #delete the account
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])

def nonstaff(request):
    if request.method == 'GET':
        all_nonstaff = User.objects.filter(is_staff = False)
        serlizer = CustomUserSerializer(all_nonstaff,many = True)
        data = {
            'message': 'success',
            'data': serlizer.data
        }
        return Response(data,status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])

def staff(request):
    if request.method == 'GET':
        all_nonstaff = User.objects.filter(is_staff = True)
        serlizer = CustomUserSerializer(all_nonstaff,many = True)
        data = {
            'message': 'success',
            'data': serlizer.data
        }
        return Response(data,status.HTTP_200_OK)