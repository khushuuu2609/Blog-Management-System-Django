# Django Model
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
#app model
from adminApp import views


urlpatterns = [
    
    path('user_detail/',views.user_detail_view, name = 'user_detail'),
    path('approve/',views.approve_view, name = 'approve'),
    path('not_approve/',views.not_approve_view, name = 'not_approve'),
    path('logout/',views.log_out_view, name = 'logout'),
    path('blog_permission/',views.blog_permission, name = 'blog_permission'),
    path('tag/',views.tag_view, name = 'tag'),
    path('category/',views.category_view, name = "category"),
    #ajax view call
    path('ajaxblogapprove/', views.ajax_blog_approve_view, name = 'ajaxblogapprove'),
    path('ajaxblogdelete/', views.ajax_blog_disapprove_view, name = 'ajaxblogdelete')

    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
