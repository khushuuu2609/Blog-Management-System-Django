from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    # Profile Model
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    #user module with one to one reationship
    mobileno = models.CharField(max_length= 11)
    avatar = models.ImageField(upload_to = 'avatars/')
    location = models.CharField(max_length = 200)
    birth_date = models.DateField(null= True)
    bio = models.TextField(max_length = 500, blank=True)

    def __str__(self):
        return self.user.username

    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    #create user profile instance
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    #save this instance
    instance.profile.save()
