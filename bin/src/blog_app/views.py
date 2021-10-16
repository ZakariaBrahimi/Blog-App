from django.shortcuts import get_object_or_404, redirect, render
from .models import Author, Post, Comment
from .forms import CreatePostForm, EditProfileForm, EditPostForm, CommentForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage
from notifications.signals import notify
from allauth.account.views import SignupView
# class HomePage(TemplateView):
#     template_name = 'home.html'


class CustomSignupView(SignupView):
    def get_context_data(self, *args, **kwargs):
        posts = Post.objects.all()
        jsonPosts = serializers.serialize('json', posts)
        ret = super(SignupView, self).get_context_data(**kwargs)
        ret.update(
            {
                'jsonPosts': jsonPosts
            }
        )
        return ret
@requires_csrf_token
def upload_image_view(request):
    f = request.FILES['image'] # Ex: myPic.png
    fs = FileSystemStorage() # class implements basic file storage on a local filesystem.
    fileName = str(f).split('.')[0] #myPic
    file = fs.save(fileName, f)
    fileUrl = fs.url(file) #Ex: /media/myPic
    print(fileUrl)
    return JsonResponse({'success': 1, 'file': {
        'url': fileUrl, 'size': fs.size(fileName), 'name': str(f), '*extesion': 'ext'
        }})

@requires_csrf_token
def upload_file_view(request):
    f = request.FILES['file']
    fs = FileSystemStorage()
    fileName = str(f).split('.')[0]
    file = fs.save(fileName, f)
    fileUrl = fs.url(file)
    return JsonResponse({'success': 1, 'file': {'url': fileUrl}})
"""
{'id': 13,
'password': '!VfZM1z4crL9Xd4jEUtOGWmJEFYm3Wtd74MkltaCV',
'last_login': datetime.datetime(2021, 10, 15, 18, 49, 2, 752899, tzinfo=<UTC>),
'is_superuser': False,
'username': 'zakaria_abdessamed',
'first_name': 'Zakaria Abdessamed ', 'last_name': 'BRAHIMI', 'email': 'za.brahimi@etu.univ-batna2.dz',
'is_staff': False, 'is_active': True, 'date_joined': datetime.datetime(2021, 10, 11, 13, 55, 15, 536311, tzinfo=<UTC>), 'img': 'avatar7.png', 'job': '', 'address': '', 'website_link': '', 'github_link': None, 'fb_link': None, 'insta_link': None, 'twitter_link': None, 'phone': None}
"""

"""
    <QuerySet [{'id': 1}, {'id': 13}]>
    14
    
    [{'id': 1}, {'id': 13}]
    """
def totalLikes(request, postID):
    print(postID)
    if request.is_ajax():
        post = get_object_or_404(Post, id=postID)
        userLikedList = list(post.likes.values('id'))
        result = list()
        for userID in userLikedList:
            result.append(userID['id'])
        if request.user.id in result:
            post.likes.remove(request.user)
            status = 'unlike'
        else:
            post.likes.add(request.user)
            status = 'like'
        totalLikes = post.totalLikes()
        return JsonResponse({'data': totalLikes, 'status': status}, safe=False)

def removeLike(request, postID):
    if request.is_ajax():
        post = get_object_or_404(Post, id=postID)
        post.likes.remove(request.user)
        totalLikes = post.totalLikes()
        return JsonResponse({'data': totalLikes}, safe=False)

def HomePage(request):
    posts = Post.objects.all()[:4]
    context = {
    'posts': posts,
    }
    searchBar(context)
    return render(request, 'home.html', context)
        
def addMoreBtnView(request, visible):
    upper = int(visible) #4
    lower = upper-4 #0
    if request.is_ajax():
        posts = Post.objects.all()[lower+1:upper]
        data = serializers.serialize('json', posts)
        return JsonResponse({'data': data}, safe=False)
    
def CommentNotification(sender_username, recipient_id):
    sender = Author.objects.get(username=sender_username)
    recipient = Author.objects.get(id=recipient_id)
    message = f"{sender} comments on your post on"
    notify.send(sender=sender, recipient=recipient, verb='Comment Notification', description=message)

def singlPost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post)
    if request.is_ajax():
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_id = request.user
            instance.post_id = post
            instance.save()
            CommentNotification(request.user.username, post.user.id)
            newComment = serializers.serialize('json', [instance, ])
            return JsonResponse({'newComment': [newComment, ]}, status=200)
        return JsonResponse({"error": "Error occured during request"}, status=400)

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        }
    searchBar(context)
    return render(request, 'singlPost.html', context)

def userProfile(request, userID):
    context = {
        'author' : Author.objects.get(id=userID),
    }
    searchBar(context)
    return render(request, 'userProfile.html', context)

def creatPost(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST or None,  request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('blog:singl_post', instance.slug)    
    else:
        form = CreatePostForm()
    context = {
        'form': form,
    }
    searchBar(context)
    return render(request, 'newPostForm.html', context)

def editPost(request, slug , postID):
    instance = get_object_or_404(Post, slug=slug, id=postID)
    if request.method == 'POST':
        form = EditPostForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('blog:singl_post', instance.slug)
    else:
        form = EditPostForm(instance=instance)
    context = {
        'post': instance,
        'form': form,
    }
    searchBar(context)
    return render(request, 'editPost.html', context)

def deletePost(request, slug, postID):
    post = get_object_or_404(Post, slug=slug, id=postID)
    if request.is_ajax():
        post.delete()
        return HttpResponse({})

def editProfile(request, userID):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:user_profile', userID)
    else:
        form = EditProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    searchBar(context)
    return render(request, 'editProfile.html', context)

def searchBar(context):
    posts = Post.objects.all()
    jsonPosts = serializers.serialize('json', posts)
    context['jsonPosts'] = jsonPosts