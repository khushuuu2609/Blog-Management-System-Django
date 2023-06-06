from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import requests
#accountapp model
from accountApp import views
from blogmanageApp.models import Post, Tag, Category

from adminApp.forms import TagForm, CategoryForm
import os

def user_detail_view(request):
    #Display the User List
    
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.filter(is_superuser = False)
        #display only the user not superuser
        context ={          
            'user':user
        }
        return render(request,'adminApp/user_display.html',context)
    else:
        return redirect('login')

def approve_view(request):
    #admin approve user account using ajax

    if request.user.is_authenticated and request.user.is_superuser:

        id = request.GET.get('user_id')
        user = User.objects.filter(id = id).update(is_staff = 1)
        return HttpResponse('success')
    
    else:
        return redirect('login')

def not_approve_view(request):
    #admin delete user account using 
    
    if request.user.is_authenticated and request.user.is_superuser:

        id = request.GET.get('user_id')
        user = User.objects.get(id = id)
        print(user.profile.avatar)
        user.profile.delete()
        user.delete()
        # Remove the user image from folder
        os.remove(user.profile.avatar.path)
        return HttpResponse('success')
    
    else:
        return redirect('login')

def log_out_view(request):
    #logout
    return redirect(views.log_out_view)

def blog_permission(request):
    # display the not approve blog 
    if request.user.is_authenticated and request.user.is_superuser:

        post = Post.objects.filter(status = False)
        return render(request, 'adminApp/blog_permission.html',{'post': post})

    else:
        return redirect('login')


def ajax_blog_approve_view(request):
    #admin approve user blog using ajax

    if request.user.is_authenticated and request.user.is_superuser:

        id = request.GET.get('post_id')
        user = Post.objects.filter(id = id).update(status = True)
        return HttpResponse('success')
    
    else:
        return redirect('login')

def ajax_blog_disapprove_view(request):
    #admin delete user blog using ajax
    
    if request.user.is_authenticated and request.user.is_superuser:

        id = request.GET.get('post_id')
        post = Post.objects.get(id = id)
        post.delete()
        return HttpResponse('success')
    
    else:
        return redirect('login')

def tag_view(request):
    tagform = TagForm(request.POST or None)
    tag_details = Tag.objects.all()
    if request.method == 'POST':
        tagform = TagForm(request.POST)
        
        if tagform.is_valid():
            tagform.save()
            return redirect(tag_view)
            
            
    return render(request,'adminApp/add_tag.html', {'tagform' : tagform, 'tag_details': tag_details})

def category_view(request):

    categoryform = CategoryForm(request.POST or None)
    category_details = Category.objects.all()

    if request.method == 'POST':
        categoryform = CategoryForm(request.POST)
        
        if categoryform.is_valid():
            categoryform.save()
            return redirect(category_view)
            
            
    return render(request,'adminApp/add_category.html', {'categoryform' : categoryform, 'category_details': category_details})

