# Generated by Django 3.2.6 on 2021-09-13 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0006_auto_20210913_1029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='comment_id',
            new_name='comments',
        ),
    ]
