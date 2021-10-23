# Generated by Django 3.2.6 on 2021-10-19 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0017_delete_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='favorites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favorite', to='blog_app.Post'),
        ),
    ]