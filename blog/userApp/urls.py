# Django Model
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
#app model
from userApp import views


urlpatterns = [
    path('index/',views.index, name = 'index'),
    path('logout/',views.log_out, name = 'logut'),
    path('update/',views.update_detail, name = 'update'),
    path('like/',views.like_view , name = 'like'),
    path('dislike/',views.dislike_view, name = 'dislike'),
    path('user_blog/',views.userblog_view, name = 'user_blog'),
    path('update_blog/<int:id>',views.updateBlog_view, name = 'update_blog'),
    path('language_test/',views.language_test_view, name = 'language_test'),

    #Ajax calling
    path('ajax_fetchdata/', views.ajax_fetchdata, name = 'ajax_fetchdata'),
    path('ajax_deleteblog/', views.ajax_blog_delete_view, name = 'ajax_deleteblog'),
    path('ajax_add_comment/', views.ajax_add_comment_view, name = 'ajax_add_comment'),
    path('ajax_add_reply/', views.ajax_add_reply_view, name = 'ajax_add_reply'),

    path('search_ajax_view/', views.search_ajax_view, name = 'search_ajax_view'),
    path('play_sound/', views.play_sound, name = 'play_sound')

    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
