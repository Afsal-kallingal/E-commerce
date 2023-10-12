from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    # path('validate/', views.validate_email, name='validate_otp'),
    path('verifyemail/',views.EmailVerification.as_view()),
    path('login/', views.login, name='login'),
    path('forget/', views.forget_password, name='forget_password'),
    path('resetpassword/', views.password_reset, name='password_reset'),
    path('changepassword/', views.password_change, name='password_change'),
    path('updateuser/', views.user_update, name='user_update'),
]