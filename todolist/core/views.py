from django.contrib.auth import (
    get_user_model,
    login,
    logout,
    authenticate
)

from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
    UpdateAPIView
)
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    SignUpSerializer,
    LoginSerializer,
    PasswordUpdateSerializer
)


User = get_user_model()


class SignUpView(CreateAPIView):
    model = User
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = SignUpSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)
        login(
            self.request,
            user=serializer.user,
            backend='django.contrib.auth.backends.ModelBackend',
        )


class SingInView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def get_queryset(self):
        return User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            login(
                request,
                user=user
            )
            user_serializer = UserSerializer(instance=user)
            return Response(user_serializer.data)
        else:
            raise AuthenticationFailed(
                'Переданы неверные учетные данные'
            )


class ProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response('', 204)


class PasswordUpdateView(UpdateAPIView):
    model = User
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = PasswordUpdateSerializer

    def get_object(self):
        return self.request.user
