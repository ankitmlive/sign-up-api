from django.urls import path
from . import views

urlpatterns = [
    # Auth url's
    path('register/', views.UserSignUpView.as_view(), name='sign-up'),
    path('login/', views.UserSignInView.as_view(), name='sign-in'),
    path('logout/', views.UserSignOutView.as_view(), name='sign-out'),
]