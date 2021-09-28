from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import Author, Comment, Followers, Like, Post
"""
    from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    class Meta:
        model = Author
        fields = '__all__'

class UserChangeForm(forms.ModelForm):
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Author
        fields = '__all__'
class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

"""
class PostList(admin.ModelAdmin):
    list_display = ('title', 'id')
admin.site.register(Author, UserAdmin)
admin.site.register(Comment)
admin.site.register(Followers)
admin.site.register(Like)
admin.site.register(Post, PostList)