from rest_framework.authtoken.views import ObtainAuthToken
from accounts.serializers import UserRegistrationSerializer, UserSerializer

from rest_framework import generics
from django.contrib.auth.models import update_last_login
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import parsers
from rest_framework import decorators

from django.contrib.auth import get_user_model
from accounts import signals
from django.contrib.auth.signals import user_logged_in

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

User = get_user_model()

#--> User List view
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def get_instance(self):
        return self.request.user

    @decorators.action(
        detail=False,
        methods=["get", "put", "patch",],
        serializer_class=UserSerializer,
        permission_classes = [IsAuthenticated]
    )
    def auth(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)

#--> auth view
class UserSignUpView(generics.CreateAPIView):
    """
    View responsible for new USER Registrartion
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        response_data = {}
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                account = serializer.save()
                response_data['response'] = 'successfully registered new user.'
        else:
            response_data = serializer.errors

        return Response(response_data)

