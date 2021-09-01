from django.shortcuts import get_object_or_404, redirect, render
from .models import Author, Post, Comment
from .forms import CreatePostForm, EditProfileForm, EditPostForm, CommentForm
from django.http import HttpResponse, JsonResponse
from django.core import serializers


def homePage(request):
    

    context = {
        'posts': Post.objects.all().order_by('-published_at'),
    }
    return render(request, 'home.html', context)







def singlPost(request, slug, postID):
    post = get_object_or_404(Post, slug=slug, id=postID)
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post)
    # if request.method == 'POST':
    #     form = CommentForm(request.POST or None)
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         instance.user_id = request.user
    #         instance.post_id = post
    #         instance.save()
    #         return redirect('blog:singl_post', post.slug, post.id)
    if request.is_ajax():
        form = CommentForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user_id = request.user
            instance.post_id = post
            instance.save()
            print(instance)
            newComment = serializers.serialize('json', [instance, ])
            print(f'new comment serialized: {newComment}')
            return JsonResponse({'newComment': [newComment, ]}, status=200)
        return JsonResponse({"error": "Error occured during request"}, status=400)
    context = {
        'post': post,
        'form': form,
        'comments': comments,
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
            return redirect('/blog')    
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
# TODO: Complete delete view funstion.
def deletePost(request, slug, postID):
    post = get_object_or_404(Post, slug=slug, id=postID)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog')
    context = {
        'post': post,
    }
    return render(request, 'deletePost.html', context)

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