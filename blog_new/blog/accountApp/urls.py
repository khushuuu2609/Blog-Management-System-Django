# Django Model
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#accountapp model
from accountApp import views

urlpatterns = [
    
    path('',views.log_in_view,name = 'login'),
    path('register/',views.register_view,name = 'register'),
    path('login/',views.log_in_view , name ='login'),
    path('logout/',views.log_out_view, name = 'logout'),
    path('password_change/',views.change_password_view, name = 'password_change'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
