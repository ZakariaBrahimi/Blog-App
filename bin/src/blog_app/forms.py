from allauth.account.forms import SignupForm, ChangePasswordForm, ResetPasswordForm, LoginForm
from .models import Post, Author, Comment
from django import forms


# to know more detials about how to custom and add css styles to a allauth forms go to the following link:
# https://gavinwiener.medium.com/modifying-django-allauth-forms-6eb19e77ef56
class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'text-md block px-3 py-2 rounded-lg w-full bg-white border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'
            })

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'text-md block px-3 py-2 rounded-lg w-full bg-white border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'
            })
            
class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomChangePasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'text-md block px-3 py-2 rounded-lg w-full bg-white border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'
            })
    
class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            if (fieldname != 'remember'):
                field.widget.attrs.update({
                    'class': 'text-md block px-3 py-2 rounded-lg w-full bg-white border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'
                })
            else:
                field.widget.attrs.update({
                    'class': 'inline text-md block px-3 py-2 rounded-lg w-full bg-white border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'
                })
                fieldname.widget.attrs.update({'class': 'inline'})


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():    
            field.widget.attrs.update({'class': 'bg-gray-200 text-md block px-3 py-2 rounded-lg w-full focus:bg-gray-100 border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'})
    class Meta:
        model = Post
        fields = '__all__'
        exclude = {'user','comment_id', 'like_id',}
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['username', 'first_name', 'last_name', 'email', 'job', 'phone', 'address', 'website_link', 'fb_link', 'insta_link', 'github_link', 'twitter_link', 'img']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': 'bg-gray-200 text-md block px-3 py-2 rounded-lg w-full focus:bg-gray-100 border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'})
        
class EditPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():    
            field.widget.attrs.update({'class': 'bg-gray-200 text-md block px-3 py-2 rounded-lg w-full focus:bg-gray-100 border-2 border-gray-300 placeholder-gray-600 shadow-md focus:placeholder-gray-500 focus:bg-white focus:border-gray-600 focus:outline-none'})

    class Meta:
        model = Post
        fields = ('title', 'img', 'content')

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': "bg-gray-100 rounded border border-gray-400 leading-normal resize-none w-full h-20 py-2 px-3 font-medium placeholder-gray-700 focus:outline-none focus:bg-white",
                'name': "body",
                'placeholder': 'Type Your Comment',
                })
            field.label = False
    class Meta:
        model = Comment
        fields = {'content',}