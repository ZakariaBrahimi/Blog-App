from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Author, Comment, Followers, Post

class PostList(admin.ModelAdmin):
    list_display = ('title', 'id')
class AuthorList(admin.ModelAdmin):
    list_display = ('email', 'username','id', )
admin.site.register(Author, AuthorList)
admin.site.register(Comment)
admin.site.register(Followers)
admin.site.register(Post, PostList)

    