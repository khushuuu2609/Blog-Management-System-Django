from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from notification.models import Notification
from django.db.models.signals import post_save
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from six import python_2_unicode_compatible
from slugify import slugify

# Create your models here.
class Category(models.Model):
     name = models.CharField(max_length= 200)
     
     def __str__(self):
         return self.name

class Tag(models.Model):
    tag_name = models.CharField(max_length= 200)

    def __str__(self):
        return self.tag_name

@python_2_unicode_compatible
class Post(models.Model):

    title = models.CharField(max_length= 200)
    title_tag = models.CharField(max_length= 200)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    tag = models.ManyToManyField(Tag)
    body = RichTextField(blank = True, null = True)
    post_date = models.DateField(auto_now_add= True)
    Category = models.ForeignKey(Category, on_delete = models.CASCADE)
    like = models.ManyToManyField(User,related_name= 'likes')
    status = models.BooleanField( default = False , null = True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')

    def get_absolute_url(self):
        return reverse("post:detail", kwargs = {'id':self.id})
         
    def total_likes(self):
        return self.like.count()

    def post(self):
        return  self.project_set.filter(like = self.pk)

    def __str__(self):
        return self.title
    
    
class UserPostComment(models.Model):

    comment = models.TextField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)    
    date = models.DateTimeField( auto_now_add= True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete = models.CASCADE)

    def total_comment(self):
        return self.comment.count()

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user
        text_preview = comment.comment[:90]
        notify = Notification(post = post, sender = sender,text_preview = text_preview, user = post.author , notification_type = 2)
        notify.save()
    
    def user_del_comment_post(sender,instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user
        del_notify = Notification.objects.filter(post = post, sender = sender, user = post.author , notification_type = 2)
        del_notify.delete()
    

#comment
post_save.connect(UserPostComment.user_comment_post, sender  = UserPostComment)
#post_save.connect(UserPostComment.user_del_comment_post, sender  = UserPostComment)
