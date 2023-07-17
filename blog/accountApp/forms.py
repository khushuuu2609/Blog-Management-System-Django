from django import forms
from django.contrib.auth.models import User

# import custom modules
from accountApp.models import Profile

class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password')
    
    def clean_password(self):
        #password validation
        password = self.cleaned_data.get('password')
        if len(password) < 4:
            raise forms.ValidationError("password is too short")
        return password

    def clean_username(self):
        #username must be unique
        name = self.cleaned_data.get('username')
        check_name = User.objects.filter(username = name ).exists()
        if check_name:
            raise forms.ValidationError("sorry this username is already register try another")
        return name
    
class ProfileForm(forms.ModelForm):

    YEARS= [x for x in range(1940,2021)]
    #year range define

    birth_date = forms.DateField(widget=forms.SelectDateWidget(years= YEARS))
    class Meta:
        model = Profile
        fields = ('mobileno','location','bio','location','avatar')
    
    def clean_mobileno(self):
        #mobileno not digit or 10 digit validation

        mobileno = self.cleaned_data.get("mobileno")
        if len(mobileno) != 10  or mobileno.isdigit() == False:
            raise forms.ValidationError('Please Enter Proper Mobile no')
        return mobileno

