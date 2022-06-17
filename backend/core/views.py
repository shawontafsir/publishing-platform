from rest_framework import views
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


class AuthenticatedApiView(views.APIView):
    pass


class UnAuthenticatedApiView(views.APIView):
    permission_classes = ()


class AuthenticatedOrReadOnlyApiView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
