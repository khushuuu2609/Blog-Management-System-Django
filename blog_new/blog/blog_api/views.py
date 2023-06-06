from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from blog_api.serializers import UserSerializer, PostSerializer
from blogmanageApp.models import Post

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


