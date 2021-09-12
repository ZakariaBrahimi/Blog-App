from django.shortcuts import get_object_or_404, redirect, render
from .models import Author, Post, Comment
from .forms import CreatePostForm, EditProfileForm, EditPostForm, CommentForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.views.generic import TemplateView, View
from django.views.decorators.csrf import requires_csrf_token
from django.core.files.storage import FileSystemStorage

# class HomePage(TemplateView):
#     template_name = 'home.html'

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

def HomePage(request):
    context = {
    'posts': Post.objects.all(),
    }
    return render(request, 'home.html', context)

class PostJsonListView(View):
    def get(self,visible, *args, **kwargs):
        print(visible)
        posts = list(Post.objects.values())
        return JsonResponse({'data': posts}, safe=False)



def singlPost(request, slug, postID):
    post = get_object_or_404(Post, slug=slug, id=postID)
    # print([post.content,])
    # ser_post = serializers.serialize('json', [post, ])
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post)
    if request.is_ajax():
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_id = request.user
            instance.post_id = post
            instance.save()
            newComment = serializers.serialize('json', [instance, ])
            return JsonResponse({'newComment': [newComment, ]}, status=200)
        return JsonResponse({"error": "Error occured during request"}, status=400)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
        # 'ser_post': ser_post,
        }
    return render(request, 'singlPost.html', context)




def userProfile(request, userID):
    context = {
        'author' : Author.objects.get(id=userID),
    }
    return render(request, 'userProfile.html', context)

def creatPost(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST or None,  request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('/')    
    else:
        form = CreatePostForm()
    context = {
        'form': form,
    }
    return render(request, 'newPostForm.html', context)

def editPost(request, slug , postID):
    instance = get_object_or_404(Post, slug=slug, id=postID)
    if request.method == 'POST':
        form = EditPostForm(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('blog:singl_post', instance.slug, instance.id)
    else:
        form = EditPostForm(instance=instance)
    context = {
        'post': instance,
        'form': form,
    }
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
    return render(request, 'editProfile.html', context)