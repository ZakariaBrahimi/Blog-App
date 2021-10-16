from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

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
    published_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Author, related_name='blog_posts', blank=True)
    def totalLikes(self):
        return self.likes.count()
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

class Followers(models.Model):
    user_id = models.ForeignKey(to='Author', on_delete=models.CASCADE)
