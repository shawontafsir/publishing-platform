from rest_framework import generics

from contents.datalayers.content import ContentDataLayer
from contents.serializers import ContentSerializer
from core.views import AuthenticatedOrReadOnlyApiView


class ContentApiView(AuthenticatedOrReadOnlyApiView, generics.ListCreateAPIView):
    serializer_class = ContentSerializer
    queryset = ContentDataLayer.get_contents()

    def get_throttles(self):
        if self.request.method == 'GET':
            return super().get_throttles()
        else:
            return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ContentDetailsApiView(AuthenticatedOrReadOnlyApiView, generics.RetrieveUpdateAPIView):
    serializer_class = ContentSerializer
    queryset = ContentDataLayer.get_contents()

    def get_throttles(self):
        if self.request.method == 'GET':
            return super().get_throttles()
        else:
            return []
