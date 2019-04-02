# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserInfo(AbstractUser):
    blog = models.OneToOneField(to='Blog')
    avatar = models.FileField(null=True, upload_to='avatar')

    def __str__(self):
        return self.username


class Blog(models.Model):
    site_name = models.CharField(max_length=100)
    site_title = models.CharField(max_length=32, null=True)
    site_style = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.site_name


class Article(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    blog = models.ForeignKey(to='Blog', db_constraint=False)
    category = models.ForeignKey(to='Category', db_constraint=False)
    content = models.TextField()
    tags = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'))
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    root_floor_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=64)
    blog = models.ForeignKey(to='Blog', db_constraint=False)

    def __str__(self):
        return self.name


class Tag(models.Model):
    blog = models.ForeignKey(to='Blog', db_constraint=False)
    name = models.CharField(max_length=32)


class Article2Tag(models.Model):
    article = models.ForeignKey(to='Article', db_constraint=False)
    tag = models.ForeignKey(to='Tag', db_constraint=False)


class Comment(models.Model):
    article = models.ForeignKey(to='Article', db_constraint=False)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    floor = models.IntegerField(null=True)
    parent_floor = models.ForeignKey(to='self', null=True)
    user = models.ForeignKey(to='UserInfo', db_constraint=False)
    reply = models.ForeignKey(to='UserInfo', db_constraint=False, null=True,related_name='reply')

    def __str__(self):
        return self.content


class LikeAndAgainst(models.Model):
    article = models.ForeignKey(to='Article', db_constraint=False)
    user = models.ForeignKey(to='UserInfo', db_constraint=False)
    like = models.BooleanField(default=False)
    against = models.BooleanField(default=False)
