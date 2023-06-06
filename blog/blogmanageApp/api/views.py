from django.db.models import Q
from rest_framework.generics import (
CreateAPIView,
ListAPIView,
RetrieveAPIView,
UpdateAPIView,
DestroyAPIView
)
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from blogmanageApp.models import Post
from blogmanageApp.api.serializer import PostSerializer, PostListSerializer
from rest_framework.permissions import IsAuthenticated

class PostCreateAPIView(CreateAPIView):
    #Create New Post API
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #chech authentication 
    permission_classes = [IsAuthenticated]

class PostDeleteAPIView(DestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class PostListAPIView(ListAPIView):
    #queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]

    #search fields here
    search_fields = ['title','title_tag']
    #for the custom pagination in the pagination class the 100 page by default value 
    pagination_class = PostPageNumberPagination #PostLimitOffsetPagination

    def get_queryset(self,*args, **kwargs):
        
        #first retrive all the object of this table
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")

        if query:
            #this is use for the filter in the current table 
            queryset_list = queryset_list.filter(Q(title__icontains = query) |
                                                Q( tag__tag_name__icontains = query) | 
                                                Q(status__icontains = query)|
                                                Q(author__first_name = query)).distinct()

        return queryset_list