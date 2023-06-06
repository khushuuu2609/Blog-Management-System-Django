from rest_framework import serializers
from blogmanageApp.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','title_tag','tag','author','body','Category','status']
    
class PostListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name = 'api-blogmanageApp:detail',
    )
    author = serializers.SerializerMethodField()
    Category = serializers.SerializerMethodField()
    #tag = serializers.SerializerMethodField()
    #avtar = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','url','title','title_tag','tag','author','body','Category','status']

    def get_author(self, obj):
        return str(obj.author.username)

    def get_Category(self, obj):
        return str(obj.Category.name)

    
