from django.urls import path, include

urlpatterns = [
    path('api/', include(('contents.api.urls', 'contents'), namespace='api'))
]
