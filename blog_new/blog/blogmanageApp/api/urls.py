# Django Model
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#blogmanageapp model
from blogmanageApp.api.views import (
PostListAPIView, 
PostDetailAPIView,
PostUpdateAPIView, 
PostDeleteAPIView,
PostCreateAPIView
)

urlpatterns = [
    path('',PostListAPIView.as_view(),name = 'list'),
    path('create/',PostCreateAPIView.as_view(), name = 'create'),
    path('<pk>/',PostDetailAPIView.as_view(),name = 'detail'),
    path('<pk>/edit',PostUpdateAPIView.as_view(),name = 'update'),
    path('<pk>/delete',PostDeleteAPIView.as_view(),name = 'delete'),



]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

