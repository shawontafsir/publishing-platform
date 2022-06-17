from django.urls import path

from contents.api.v1 import views

urlpatterns = [
    path('', views.ContentApiView.as_view(), name='content_api_view'),
    path('<str:pk>', views.ContentDetailsApiView.as_view(), name='content_details_api_view')
]
