from rest_framework.authtoken.views import ObtainAuthToken
from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer

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

class UserSignInView(ObtainAuthToken):
    """
    View responsible for USER Login
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        response_data = {}
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                token, created = Token.objects.get_or_create(user=user)
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                update_last_login(None, user)
                response_data['details'] = 'successfully logged in'
                # response_data['email'] = user.email
                # response_data['fullname'] = user.fullname
                # response_data['username'] = user.username
                # response_data['avatar'] = request.build_absolute_uri(user.avatar.url)
                #response_data['pk'] = user.pk
                response_data['token'] = token.key
        else:
            response_data = serializer.errors

        return Response(response_data)

class UserSignOutView(APIView):
    """
    View responsible for USER Signout
    later there is a need of serializer implementaion
    """
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        response_data = {}
        data = Token.objects.filter(user=request.user).delete()
        response_data['response'] = 'user successfully logged out'
        return Response(response_data)