from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    path('register/', views.SignUp.as_view(), name='register'),
    path('signin/', auth_views.LoginView.as_view(template_name="accounts/signin.html"), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name="signout"),
    #path('profile/', name="profile"),
]

