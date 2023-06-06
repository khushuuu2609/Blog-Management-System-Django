from django.db import models
#from blogmanageApp.models import Post
from django.contrib.auth.models import User
# Create your models here.
class Notification(models.Model):
    
    NOTIFICATION_TYPE = ((1,'Like'),(2,'Comment'))

    post = models.ForeignKey('blogmanageApp.Post', on_delete = models.CASCADE,related_name = 'noti_post', blank= True, null= True)
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'noti_from_user', blank= True, null= True )
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'noti_to_user', blank= True, null= True )
    notification_type = models.IntegerField(choices=  NOTIFICATION_TYPE)
    text_preview = models.CharField(max_length= 90, blank= True)
    date = models.DateTimeField(auto_now_add= True)
    is_seen = models.BooleanField(default= False)
