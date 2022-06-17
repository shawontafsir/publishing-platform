from django.urls import path, include

urlpatterns = [
    path('v1/', include(('contents.api.v1.urls', 'contents'), namespace='v1'))
]
