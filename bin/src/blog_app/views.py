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
from django.contrib.auth.decorators import login_required


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
# =================================================================================================

def followingView(request, userID):
    if request.is_ajax():
        author = get_object_or_404(Author, id=request.user.id)
        result = []
        for user in list(author.followers.values()):
            result.append(user['id'])
            print(f'result ===>> {result}')
        if int(userID) in result:
            print('unfollowing')
            status = 'unfollow'
            author.followers.remove(userID)
            print(f'unfollow result ===>> {result}')
        else:
            status = 'follow'
            print('following')
            author.followers.add(userID)
            print(f'follow result ===>> {result}')
        totalFollowers = author.totalFollowers()
        print(totalFollowers)
        return JsonResponse({'totalFollowers': totalFollowers, 'status': status}, safe=False)
    
# =================================================================================================

def favoriteList(request):
    user = request.user
    favoriteList = user.favorites.all()
    
    context = {
        'favoriteList': favoriteList,
    }
    return render(request, 'bookmarksList.html', context)
    
def favoriteView(request, postID):
    if request.is_ajax():
        author = request.user
        post = get_object_or_404(Post, id=postID)
        print(post.id in list(post.user.favorites.values('id')))
        result = []
        for post in list(author.favorites.values()):
            result.append(post['id'])
        if int(postID) in result:
            print('removing')
            status = 'unbooked'
            author.favorites.remove(postID)
        else:
            status = 'booked'
            print('adding')
            author.favorites.add(postID)
        favoriteList = author.favoriteList()
        print(favoriteList)
        return JsonResponse({'favoriteList': favoriteList, 'status': status}, safe=False)



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



def HomePage(request):
    posts = Post.objects.all()[:] # Post.objects.all()[:4] ===>> for load more data ( loading by 4 posts)
    context = {
    'posts': posts,
    }
    searchBar(context)
    return render(request, 'home.html', context)
        
def addMoreBtnView(request, visible):
    upper = int(visible) #4
    lower = upper-4 #0
    if request.is_ajax():
        allPosts = serializers.serialize('json', Post.objects.all())
        # post = get_object_or_404(Post, id=postID)
        posts = Post.objects.all()[lower+1:upper]
        # authors = posts.user
        users = list(posts.values('user_id'))
        result = list()
        for userID in users:
            result.append(userID['user_id'])
        final_result = list(set(result))
        for i in final_result:
            users = Author.objects.filter(id=i)
        data = serializers.serialize('json', posts)
        
        return JsonResponse({'data': data, 'allPosts': allPosts}, safe=False)
    
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
    form = EditPostForm(instance=instance)
    if request.user.is_authenticated and request.user.id == instance.user.id:
        if request.method == 'POST':
            form = EditPostForm(request.POST or None, request.FILES or None, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('blog:singl_post', instance.slug)
            else:
                form = EditPostForm(instance=instance)    
    else:
        return redirect('blog:singl_post', instance.slug)
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

@login_required(login_url='/accounts/login/')
def editProfile(request, userID):
    instance = get_object_or_404(Author, id=userID)
    form = EditProfileForm(instance=request.user)
    if request.user.is_authenticated and request.user.id == instance.id:
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
    users = Author.objects.all()
    jsonPosts = serializers.serialize('json', posts)
    jsonUsers = serializers.serialize('json', users)
    context['jsonPosts'] = jsonPosts
    # context['jsonUsers'] = jsonUsers