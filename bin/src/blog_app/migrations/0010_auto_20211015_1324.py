# Generated by Django 3.2.6 on 2021-10-15 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0009_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like_id',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]