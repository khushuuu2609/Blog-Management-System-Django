from django.contrib.auth.models import User
from rest_framework import serializers
from blogmanageApp.models import Post
from accountApp.models import Profile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email','password']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Post
        fields = ['url','title', 'body','author']