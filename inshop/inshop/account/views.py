from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view,APIView,parser_classes,permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser,FileUploadParser
from .permissions import IsAuthenticated
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.authtoken.models import Token
from .models import Account
from django.contrib.sessions.backends.db import SessionStore
from .serializers import AccountSerializer,PasswordChangeSerializer,PasswordResetSerializer
from random import randint


@api_view(['POST'])
@parser_classes([JSONParser,FormParser, MultiPartParser,FileUploadParser])
@permission_classes([AllowAny])
def register(request):
    status_code=status.HTTP_400_BAD_REQUEST
    if request.method == 'POST':
        data = {}
        email = request.data.get('email', '0').lower()
        print(email)
        request_data = request.data.copy()
        serializer = AccountSerializer(data=request_data)
        if serializer.is_valid():
            status_code=status.HTTP_200_OK
            data= serializer.data
            otp = randint(1000,9999)
            # to_email = request.data.get('email')
            # subject = "OTP verification"
            # html_context = {
            #     "title":"OTP verification",
            #     "data":[
            #         {
            #             "label":"Your OTP is : ",
            #             "value":otp
            #         }
            #     ]
            # }
            # text_content = str(html_context)
            # send_mail(html_context,to_email,subject)
            # subject = 'Hello, Django Email'
            # message = 'This is a test email sent from Django using Google SMTP.'
            # from_email = 'muhsinpmoosi2305@gmail.com'  # Should match EMAIL_HOST_USER
            # recipient_list = [to_email]
            # send_mail(subject, message, from_email, recipient_list)

            my_session = SessionStore()
            my_session['email'] = request.data.get('email')
            # my_session['username'] = request.data.get('username')
            my_session['password'] = request.data.get('password')
            my_session['name'] = request.data.get('name')
            my_session['address'] = request.data.get('address')
            my_session['otp'] = otp
            my_session['login_otp_count'] = 5
            my_session.create()
            data['session_key'] = my_session.session_key
            print(my_session['otp'])
        else:
            data = serializer.errors
            status_code=status.HTTP_400_BAD_REQUEST
        return Response(data,status=status_code)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def validate_email(email):
#     user = None
#     try:
#         user = Account.objects.get(email=email)
#         # print(user)
#     except Account.DoesNotExist:
#         return None
#     if user != None:
#         return email
    
class EmailVerification(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        session_key = request.data.get('session_key')
        my_session = SessionStore(session_key=session_key)

        data = {}
        otp = request.data['otp']
        otp_verification = my_session['otp']
        if ((int(otp) == int(otp_verification))and (my_session['login_otp_count'] > 0)):

            request_data = request.data.copy()
            request_data['email'] = my_session['email']
            request_data['password'] = my_session['password']
            request_data['name'] = my_session['name']
            request_data['address'] = my_session['address']
            # request_data['username'] = my_session['username']

            serializer = AccountSerializer(data=request_data)
            if serializer.is_valid():
                user = serializer.save()
                data['response'] = 'successfully registered new user.'
                data['email'] = user.email
                # data['username'] = user.username
                data['pk'] = user.pk

                try:
                    token = Token.objects.get(user=user).key
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user).key
                    
                data['token'] = token
                data['response'] = "Email Verfied Successfully"
                status_code=status.HTTP_200_OK
            else:
                data = serializer.errors
                status_code=status.HTTP_400_BAD_REQUEST
            return Response(data,status=status_code)
        

        else:
            if(my_session['login_otp_count'] > 0):
                my_session['login_otp_count'] -= 1
                data['error_message'] = "invalid OTP"
            else:
                my_session.delete()
                data['error_message'] = "Limit Exceeded, Register again"

            status_code=status.HTTP_400_BAD_REQUEST
        return Response(data,status=status_code)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user=authenticate(request, email=email, password=password)
#         if user is not None:
#             auth_login(request, user)
#             return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
            
        
#         return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
# from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful.', 'token': token.key}, status=status.HTTP_200_OK)
            
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def forget_password(request):
    email=request.data.get('email')
    user=Account.objects.get(email=email)
    if user:
        otp=randint(1000,9999)
        print(otp)
        user.otp=otp
        user.save() 
        return Response({'message': 'OTP sent successfully'},status=status.HTTP_200_OK)
    else:
        return Response({'message': 'invalid cridential'},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    if request.method == 'POST':
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                user = Account.objects.get(email=email,otp=otp)
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                return Response({'message': 'Invalid username or OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def password_change(request):
    if request.method == 'POST':
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if user.check_password(old_password):
                try:
                    user.set_password(new_password)
                    user.save()
                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
                except Account.DoesNotExist:
                    return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def user_update(request):
#     user=request.user
#     if request.method == 'PUT':
#         serializer = AccountSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             user.is_verified = False
#             otp=randint(100000,999999)
#             print(otp)
#             user.otp=otp
#             password=serializer.validated_data['password']
#             user.set_password(password)
#             user.save()            
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_update(request):
    if request.method == 'PUT':
        user = request.user
        serializer = AccountSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user.is_verified = False
            otp=randint(100000,999999)
            print(otp)
            user.otp=otp
            user.save()
            serializer.save()
            if user:
                password=serializer.validated_data['password']
                if password:
                    user.set_password(password)
                    user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)