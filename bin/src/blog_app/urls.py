from django.conf.urls import url
from . import views
app_name = 'blog_app'
urlpatterns = [
    url(r'^$', views.homePage, name='home_page'),
    url(r'^singl-post/(?P<slug>[-\w]+)/(?P<postID>\d+)/$', views.singlPost, name='singl_post'),
    url(r'^profile/(?P<userID>\d+)/$', views.userProfile, name='user_profile'),
    url(r'^create-post/$', views.creatPost, name='create_post'),
    url(r'^delete-post/(?P<slug>[-\w]+)/(?P<postID>\d+)/$', views.deletePost, name='delete_post'),
    url(r'^edit-post/(?P<slug>[-\w]+)/(?P<postID>\d+)/$', views.editPost, name='edit_post'),
    url(r'^edit-profile/(?P<userID>\d+)/$', views.editProfile, name='edit_profile'),
]
