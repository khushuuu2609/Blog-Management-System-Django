from django import forms
from accountApp.models import Profile
from django.contrib.auth.models import User
from blogmanageApp.models import Post, UserPostComment

class UpdateProfileForm(forms.ModelForm):
    # update user profile module form
    
    class Meta:
        model = Profile
        fields = ('mobileno','avatar', 'location', 'birth_date', 'bio')

class UpdateUserForm(forms.ModelForm):
    # update user module form
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class CommentForm(forms.ModelForm):
    #comment form 
    class Meta:
        model = UserPostComment
        fields = ('comment',) 