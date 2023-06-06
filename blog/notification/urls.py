# Django Model
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#blogmanageapp model
from notification import views
from notification.views import PostDetailView
urlpatterns = [
    
    path('',views.notification_view,name = 'notification'),
    path('delete/<int:id>',views.DeleteNotificationView,name = 'delete'),
    path('post/<pk>', PostDetailView.as_view(), name='post'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
