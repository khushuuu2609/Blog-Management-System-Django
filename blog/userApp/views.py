from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from itertools import zip_longest as zl
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
import json
from django.db.models import Q
import os

#custom App modules
from accountApp import views
from accountApp.models import Profile
from userApp.forms import UpdateProfileForm, UpdateUserForm
from blogmanageApp.models import Post, UserPostComment
from blogmanageApp.forms import PostForm
from userApp.forms import CommentForm
from googletrans import Translator
from django.utils.translation import gettext as _
from notification.models import Notification
import multiprocessing
from playsound import playsound

@login_required(login_url= 'login') 
def index(request):

    id = request.session['id']
    user_profile = User.objects.filter(id = id)
    
    #ajax call'
    '''
    print(request.method)
    if request.method == "GET":
        search_text = request.GET.get('search_text')
        
        if search_text is not None and search_text != u"":
            search_text = request.GET.get('search_text')
            post = Post.objects.filter(title__istartswith = search_text).filter(status = True).order_by('-post_date')
            
        else:
            post = []
            post = Post.objects.filter(status = True).order_by('-post_date')
    '''

    post = Post.objects.filter(status = True ).order_by('-post_date')

    paginator = Paginator(post,10)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    
    except PageNotAnInteger:
        posts = paginator.page(1)

    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    
    post_id = Post.objects.filter(author = id , status = True)
    comment = UserPostComment.objects.all()
    comment_filter = UserPostComment.objects.values('post_id' ).annotate(total = Count('user_id')).filter(parent_id = None)
    
    context ={

        'user_profile':user_profile,
        'post_detail': post,
        'comment' : comment,
        'comment_filter' : comment_filter,
        'page' : page,
        'posts' : posts,
        
    }
    return render(request,'userApp/index.html',context)

def search_ajax_view(request):

    if request.method == "GET":
        search_text = request.GET.get('search_text')

        if search_text is not None and search_text != u"":
            search_text = request.GET.get('search_text')
            post = Post.objects.filter(Q(title__istartswith = search_text) | Q(tag__tag_name__istartswith = search_text)| Q(post_date__istartswith = search_text) | 
                                                            Q(title_tag__istartswith = search_text)).filter(status = True).order_by('-post_date')
        else:
            post = []
            
            post = Post.objects.filter(status = True).order_by('-post_date')

        search_paginator = Paginator(post,10)

        page = request.GET.get('page')

        try:
            posts = search_paginator.page(page)
        
        except PageNotAnInteger:
            posts = search_paginator.page(1)

        except EmptyPage:
            posts = search_paginator.page(paginator.num_pages)

    
        id = request.session['id']
        user_profile = User.objects.filter(id = id)
        post_id = Post.objects.filter(author = id , status = True)
        comment = UserPostComment.objects.all()
        comment_filter = UserPostComment.objects.values('post_id' ).annotate(total = Count('user_id'))
        data = post.values()

        context ={

            'post_detail': post,
            'comment' : comment,
            'comment_filter' : comment_filter,
            'posts_d' : posts,
            'page' : page,

        }

        return render(request,'userApp/search_result.html',context)

    

@login_required(login_url= 'login') 
def log_out(request):
    #calling auccount logout module
    return redirect(views.log_out)

@login_required(login_url= 'login') 
def update_detail(request):
    
    id = request.session['id']
    instance = Profile.objects.get(user_id=id)
    instance2 = User.objects.get(id = id)

    # set user detail using this instance
    userform = UpdateUserForm(request.POST or None, instance= instance2)
    profileform = UpdateProfileForm(instance= instance)

    if request.method == 'POST':
        
        profileform = UpdateProfileForm(request.POST, request.FILES , instance = instance)
        userform = UpdateUserForm(request.POST or None, instance= instance2)

        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            return redirect('index')

    return render(request,'userApp/update_detail.html',{ 'form':profileform, 'userform':userform })


@login_required(login_url= 'login') 
def like_view(request):
    #ajax calling

    id = request.session['id']
    post_id = request.GET.get('post_id')
    post = Post.objects.filter(id = post_id)
    
    author = []
    for i in post:
        author.append(i.author_id)

    post_data = Post(id= post_id)
    users = User.objects.filter(id = id)
    post_data.like.add(id)

    print(post_data.count(),"$$$$$")
    #print(post.author)
    notify = Notification(post_id = post_id, sender_id = id, user_id = author[0] , notification_type = 1)
    notify.save()

    return HttpResponse('success')

@login_required(login_url= 'login') 
def dislike_view(request):
    #ajax calling

    id = request.session['id']
    post_id = request.GET.get('post_id')

    post_data = Post(id= post_id)
    users = User.objects.filter(id = id)
    post_data.like.remove(id)
    return HttpResponse('success')

@login_required(login_url= 'login') 
def userblog_view(request):
    #Display only own user blog

    id = request.session['id']
    post = Post.objects.filter(author = id)
    return render(request,'userApp/user_blog.html',{'post': post})

@login_required(login_url='login')
def updateBlog_view(request, id):
    # user Own blog update

    post_id = id
    post = Post.objects.get(id = post_id)
    user_id = request.session['id']

    #user can onliy access own blog
    if user_id == post.author.id :
        blogform = PostForm(request.POST or None, initial={ "status": False}, instance= post )

        if request.method == "POST":
            
            blogform = PostForm(request.POST, request.FILES  ,instance = post  )
            if blogform.is_valid():
                
                blogform.save( )
                return redirect('index')
    else:
        return redirect(userblog_view)

    return render(request,'userApp/update_blog.html',{ 'blogform': blogform })

@login_required(login_url='login')
def ajax_fetchdata(request):
    # like details display

    post_id = request.GET.get('post_id')
    id = request.session['id']
    post = Post.objects.filter(id = post_id)
    
    author = []
    for i in post:
        author.append(i.author_id)

    post_data = Post(id= post_id)
    users = User.objects.filter(id = id)
    post_data.like.add(id)
    #print(post.author)
    notify = Notification(post_id = post_id, sender_id = id, user_id = author[0] , notification_type = 1)
    notify.save()
    post = Post.objects.get(id = post_id)
    post_name = post.like.all()
    comment_detail = UserPostComment.objects.all()
    # total like display
    post_detail = post.like.count()
    print(post_detail, "FFFF")
    context = {
        'post_detail': post_detail,
    }
    return JsonResponse(context)


@login_required(login_url='login')
def ajax_blog_delete_view(request):
    #admin delete user account using 
    
    id = request.GET.get('post_id')
    post = Post.objects.get(id = id)
    post.delete()
    return HttpResponse('success')

@login_required(login_url='login')
def ajax_add_comment_view(request):
    #admin delete user account using 
    
    id = int(request.GET.get('post_id'))
    user = int(request.session['id'])    
    comment = request.GET.get('comment')
    userpostcomment = UserPostComment.objects.create(comment = comment, user_id = user, post_id = id)
    #userpostcomment.save()
    parent_obj = None
    comment_form = CommentForm(data=request.POST)

    try:
        parent_id = int(request.POST.get('parent_id'))
    except:
        parent_id = None

    if parent_id:
        parent_obj = UserPostComment.objects.get(id=parent_id)
        # if parent object exist
        if parent_obj:
            # create replay comment object
            replay_comment = comment_form.save(commit=False)
            # assign parent_obj to replay comment
            replay_comment.parent = parent_obj
    
    comment_obj = UserPostComment.objects.all()
    context = {
        'comment': comment
    }
    return JsonResponse(context)

@login_required(login_url='login')
def ajax_add_reply_view(request):
    #admin delete user account using 
    
    id = int(request.GET.get('comment_id'))
    post = int(request.GET.get('post_id'))
    user = int(request.session['id'])    
    reply = request.GET.get('reply')
    parent_obj = None

    try:
        parent_id = int(request.GET.get('comment_id'))
    except:
        parent_id = None

    if parent_id:
        parent_obj = UserPostComment.objects.get(id = parent_id)
        # if parent object exist
        if parent_obj:
            # create replay comment object
            p = UserPostComment.objects.create(comment = reply, parent = parent_obj, user_id = user, post_id = post )
            p.save()
            # assign parent_obj to replay comment
            #reply.parent = parent_obj
    
    comment_obj = UserPostComment.objects.all()
    context = {
        'reply': reply
    }
    return JsonResponse(context)

def language_test_view(request):
    text  =_("Welcome to my site.")
    return render(request,'userApp/language_test.html',{'text' : text})

def play_sound(request):
    p = multiprocessing.Process(target=playsound, args=("welcome2.mp3",))
    p.start()
    p.terminate()
    
    return HttpResponse('success')