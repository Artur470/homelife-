from django.urls import path
from .views import *
from users.models import User
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('me/', UserMeView.as_view(), name='profile'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('wholesaler-otp/', WholesalerOTPVerificationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('confirm-code/', ConfirmCodeView.as_view(), name='confirm-code'),
    path('change-forgot-password/', ChangeForgotPasswordView.as_view(), name='change-forgot-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('user-list/', UserListView.as_view(), name='user-list'),
]
