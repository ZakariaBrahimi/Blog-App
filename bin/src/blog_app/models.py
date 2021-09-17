from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django_editorjs import EditorJsField


class Author(AbstractUser):
    img = models.ImageField(default='avatar7.png', upload_to='user_imgs', null=True, blank=True)
    job = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    website_link = models.URLField()
    github_link = models.URLField(blank=True, null=True)
    fb_link = models.URLField(blank=True, null=True)
    insta_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Post(models.Model):
    user = models.ForeignKey('Author', on_delete = models.CASCADE, blank=True, null=True)
    slug = models.SlugField(editable=False, default='', blank=True, null=True)
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to='notes_img')
    content = models.TextField()
    # EditorJsField(editorjs_config={
    #     "tools":{
    #         "Image":{
    #             "config":{
    #                 "endpoints":{
    #                     "byFile": "/imageUPload/",
    #                     "byUrl": "/imageUPload/",
    #                             },
    #                     "additionalRequestHeaders": [{"Content-Type": "multipart/form-data"}]
    #                     }},
    #         "Attachs":{
    #            "config":{
    #                 "endpoint": "/fileUPload/",
    #                 "additionalRequestHeaders": [{"Content-Type": "multipart/form-data"}],
    #                     }}}
    #     })
    published_at = models.DateTimeField(auto_now_add=True)
    # comment_id = models.ForeignKey(to='Comment', on_delete=models.CASCADE, blank=True, null=True)
    like_id = models.ForeignKey(to='Like', on_delete=models.CASCADE, blank=True, null=True)
    # totalComments = user.comment_set.all()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post_id = models.ForeignKey(to='Post', on_delete=models.CASCADE, blank=True, null=True)
    user_id = models.ForeignKey(to='Author',on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    def __str__(self):
        return f"commented by {self.user_id.first_name} on {self.post_id.title}'s post"

class Like(models.Model):
    user_id = models.ForeignKey(to='Author', on_delete=models.CASCADE)
    post_id = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    
class Followers(models.Model):
    user_id = models.ForeignKey(to='Author', on_delete=models.CASCADE)
