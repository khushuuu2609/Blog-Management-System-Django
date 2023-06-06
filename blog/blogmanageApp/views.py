from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#custom models
from blogmanageApp.forms import PostForm
from userApp.views import index
# Create your views here.

@login_required(login_url= 'login')
def blog_view(request):
    # add blog

    id = request.session['id']
    instance1 = User.objects.filter(id = id).first()

    #set status initial value and author initial value set
    postform = PostForm(request.POST or None, initial={ "status": False ,"author": id  }, instance= instance1)
    
    if request.method == 'POST':
        postform = PostForm(request.POST)
        
        if postform.is_valid():
            author = postform.cleaned_data['author']
            print(author)
            postform.save()
            return redirect(index)
            
    return render(request,'blogmanage/blog.html', {'postform' : postform})
