from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView 
from authentication.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.
# manualy genarate Token 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class Register(APIView):
    def post(self, request, fromat=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token ,"msg":"Registration success"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class Login(APIView):
    def post(self, request, fromat=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get("email")
            password=serializer.data.get("password")
            user = authenticate(email=email , password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({"token":token,"msg":"Login Success"},status=status.HTTP_200_OK)
            else:
                return Response({"errors":{'none_field_error':['Email or Password is not validate']}},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        
class Profile(APIView):
    permission_classes=[IsAuthenticated]
    def get (self,request,format=None):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data ,status=status.HTTP_200_OK)
    
class ChangePassword(APIView):
    permission_classes=[IsAuthenticated]
    def post (self ,request,format=None):
        serializer=ChangePasswordSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response ({"msg":'password change successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        