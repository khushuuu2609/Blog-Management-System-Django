from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class PostLimitOffsetPagination(LimitOffsetPagination):
    #overide the Limitoffsetpagination here 
    default_limit = 2
    max_limit = 10

class PostPageNumberPagination(PageNumberPagination):
    #number of recodes display in the current page override the pagenumberpagination 
    page_size = 3