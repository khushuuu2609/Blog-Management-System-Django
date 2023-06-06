
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from notification.models import Notification
#custom models
from userApp.views import index
from django.db.models import Q
from hitcount.views import HitCountDetailView
from blogmanageApp.models import Post
from django.utils.decorators import method_decorator

# Create your views here.

@login_required(login_url= 'login')
def notification_view(request):
    user = int(request.session['id'])    
    notification =  Notification.objects.filter(user = user).filter(~Q(sender = user)).order_by('-date')
    Notification.objects.filter(user = user, is_seen = False).update(is_seen = True)
    return render(request, 'notification/notification.html',{'notification' : notification})

@login_required(login_url= 'login')
def DeleteNotificationView(request, id):
    
    user = int(request.session['id'])   
    print('notification:',id) 
    Notification.objects.filter( id = id, user = user).delete()
    return redirect(notification_view)

def CountNotificationView(request):
    count_notification = 0
    if request.user.is_authenticated: 
        if request.user.is_superuser :
            pass
        else: 
            user = int(request.session['id'])
            count_notification = Notification.objects.filter(user = user, is_seen = False).filter(~Q(sender = user)).count()
    return {'count_notification': count_notification}

@method_decorator(login_required, name='dispatch')
class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'notification/post_view.html'
    context_object_name = 'post'
    slug_field = 'slug'

    # set to True to count the hit
    count_hit = True
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        post = Post.objects.filter(status = True).filter(id = self.kwargs['pk']).order_by('-post_date')
        context.update({
        'popular_posts': Post.objects.order_by('-hit_count_generic__hits')[:3],
        'posts':post
        })
        return context

