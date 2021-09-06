from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django_editorjs import EditorJsField


class Author(AbstractUser):
    img = models.ImageField(default='avatar7.png', upload_to='user_imgs', null=True, blank=True)
    job = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    website_link = models.URLField()
    github_link = models.URLField(default='/')
    fb_link = models.URLField(default='/')
    insta_link = models.URLField(default='/')
    twitter_link = models.URLField(default='/')
    phone = models.IntegerField(default=3203804539)

class Post(models.Model):
    user = models.ForeignKey('Author', on_delete = models.CASCADE, blank=True, null=True)
    slug = models.SlugField(editable=False, default='', blank=True, null=True)
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='notes_img')
    content = EditorJsField(editorjs_config={
        "tools":{
                "Image":{
                        "config":{
                                "endpoints":{
                                            "byFile": "/imageUPload/",
                                            "byUrl": "/imageUPload/",
                                },
                                "additionalRequestHeaders": [{"Content-Type": "multipart/form-data"}]
                        }
                },
                "Attachs":{
                        "config":{
                                "endpoint": "/fileUPload/",
                                "additionalRequestHeaders": [{"Content-Type": "multipart/form-data"}],
                        }
                }
        }
        })
    published_at = models.DateTimeField(auto_now_add=True)
    comment_id = models.ForeignKey(to='Comment', on_delete=models.CASCADE, blank=True, null=True)
    like_id = models.ForeignKey(to='Like', on_delete=models.CASCADE, blank=True, null=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    post_id = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    user_id = models.ForeignKey(to='Author',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

class Like(models.Model):
    user_id = models.ForeignKey(to='Author', on_delete=models.CASCADE)
    post_id = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    
class Followers(models.Model):
    user_id = models.ForeignKey(to='Author', on_delete=models.CASCADE)
