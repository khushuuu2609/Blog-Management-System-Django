# Django Model
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#blogmanageapp model
from blogmanageApp import views

urlpatterns = [
    
    path('blog/',views.blog_view,name = 'blog'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

