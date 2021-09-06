from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'blog_app'
urlpatterns = [
    url(r'^$', views.HomePage, name='home_page'),
    url(r'^posts/(?P<visible>\d+)/$', views.PostJsonListView.as_view(), name='posts'),
    url(r'^singl-post/(?P<slug>[-\w]+)/(?P<postID>\d+)/$', views.singlPost, name='singl_post'),
    url(r'^profile/(?P<userID>\d+)/$', views.userProfile, name='user_profile'),
    url(r'^create-post/$', views.creatPost, name='create_post'),
    url(r'^delete-post/(?P<slug>[-\w]+)/(?P<postID>\d+)/$', views.deletePost, name='delete_post'),
    url(r'^edit-post/(?P<slug>[-\w]+)/(?P<postID>\d+)/$', views.editPost, name='edit_post'),
    url(r'^edit-profile/(?P<userID>\d+)/$', views.editProfile, name='edit_profile'),
    url(r'^fileUPload/$', csrf_exempt(views.upload_file_view)),
    url(r'^imageUPload/$', csrf_exempt(views.upload_image_view)),
]
