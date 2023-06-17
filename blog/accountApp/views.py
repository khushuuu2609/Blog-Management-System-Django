from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

# django custom modules
from .forms import ProfileForm, UserForm
from .models import Profile
# import make_password encrypt form
from django.contrib.auth.hashers import make_password
from adminApp.views import user_detail_view
from userApp.views import index

# Create your views here.
def register_view(request):
    # Registraion view for user
    userform = UserForm()
    profileform = ProfileForm()
    
    if request.method == "POST":

        userform = UserForm(request.POST or None)
        profileform = ProfileForm(request.POST,request.FILES)
        #both form is valid check
        if userform.is_valid() and profileform.is_valid():
            # create user model object
            user = userform.save(commit=False)
            user.password = make_password(userform.cleaned_data.get('password'))
            user.save()
            user.refresh_from_db()

            user.profile.mobileno = profileform.cleaned_data.get('mobileno')
            user.profile.avatar = profileform.cleaned_data.get('avatar')
            user.profile.bio = profileform.cleaned_data.get('bio')
            user.profile.birth_date = profileform.cleaned_data.get('birth_date')
            user.profile.location = profileform.cleaned_data.get('location')
            #save profile instance
            user.save()
            return redirect('login')
    
    context = {
        'userform': userform,
        'profileform' : profileform 
    }
    
    return render(request,'accountApp/register.html',context)
    
def log_in_view(request):
    #user and admin both use this login view

    if request.user.is_authenticated:
        
        if request.user.is_superuser:
            return redirect(user_detail_view)
        
        else:
            return redirect(index)

    else:

        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username , password = password)
            #authentication check
            error_message = ""
            if user and user.is_staff:

                # check admin Approval
                login(request, user)

                if user.is_superuser :
                    request.session['id'] = user.id

                    #check user is superuser or not
                    return redirect('user_detail')
                
                else:
                    request.session['id'] = user.id
                    return redirect('index')
                
            else:
                    error = "Please Enter valid username and password or your account not approved by admin"
            
            return render(request,'accountApp/login.html',{ 'error_message': error })

        else:
            return render(request,'accountApp/login.html')

def log_out_view(request):
    # user and admin both use this logout view
    
    logout(request)
    if logout(request):
        try:
            return redirect(log_in)
            
        except Exception as e:
            return HttpResponse("Something Wrong", e)
    else:
        return redirect(index)

def change_password_view(request):

    if request.method  == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect(index)
        else:
            return render(request,'accountApp/changepassword.html', {'form' : form})    
    else:
        form = PasswordChangeForm(request.user)
        return render(request,'accountApp/changepassword.html', {'form' : form})