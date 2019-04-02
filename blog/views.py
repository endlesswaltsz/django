import datetime
import io
import random

from PIL import Image, ImageDraw, ImageFont
from django.contrib import auth
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from rest_framework.views import APIView
from rest_framework import serializers
from blog import customform
from blog import models


# Create your views here.

def register(request):
    if request.method == 'GET':
        form = customform.UserForm()
        return render(request, 'register.html', locals())
    form = customform.UserForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        head = request.FILES.get('head')
        blog = models.Blog.objects.create(site_name=username)
        models.UserInfo.objects.create_user(
            username=username, password=password, email=email, avatar=head, blog=blog)
        return JsonResponse({'status': 'success', 'url': '/login/'})
    else:
        return JsonResponse({'status': 'error', 'msg': form.errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    ran_code = request.POST.get('ran_code')
    if ran_code.upper() != request.session['random_code'].upper():
        return JsonResponse({'status': 'error', 'msg': '验证码错误!'})
    if user:
        auth.login(request, user)
        return JsonResponse({'status': 'success', 'url': 'http://172.96.198.74'})
    return JsonResponse({'status': 'error', 'msg': '账号或密码错误!'})


def logout(request):
    auth.logout(request)
    return redirect('http://172.96.198.74')


def index(request):
    articles = models.Article.objects.all().order_by('-upload_time')
    paginator = Paginator(articles, 5)
    page_num = request.GET.get('page')
    if page_num:
        if page_num.isdigit():
            page_num = int(page_num)
        else:
            return render(request, 'error.html')
    if not page_num:
        page_num = 1
    if page_num > paginator.num_pages:
        page_num = paginator.num_pages
    if page_num < 1:
        page_num = 1
    page = paginator.page(page_num)
    if paginator.num_pages <= 5:
        page_range = paginator.page_range
    else:
        if page_num < 4:
            page_range = range(1, 6)
        elif page_num + 3 > paginator.num_pages:
            page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            page_range = range(page_num - 2, page_num + 3)
    return render(request, 'index.html', {'pages': page, 'range': page_range, 'paginator': paginator})


def random_code():
    code = ''
    for i in range(4):
        code += random.choice(
            [chr(random.randint(97, 122)), chr(random.randint(65, 90)), str(random.randint(0, 9))])
    return code


def random_image(request):
    img = Image.new('RGB', (150, 30), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    image_font = ImageFont.truetype('static/font/genesis.woff.ttf', 25)
    image_draw = ImageDraw.Draw(img)
    text = random_code()
    request.session['random_code'] = text
    for i in range(4):
        image_draw.text((25 + i * 30, 0), text[i], font=image_font)
    f = io.BytesIO()
    img.save(f, 'png')
    return HttpResponse(f.getvalue())


def site_detail(request, username, func, num):
    user = models.UserInfo.objects.get(username=username)
    if not (user and func == 'category' or 'archive' or 'tag' and num.isdigit()):
        return render(request, 'error.html')
    blog = models.Blog.objects.filter(userinfo__username=username)
    if func == 'category':
        category = models.Category.objects.filter(blog=blog, pk=num).first()
        if category:
            return render(request, 'site_detail.html', {'category': category, 'user': user})
        else:
            return render(request, 'error.html')
    elif func == 'tag':
        tag = models.Tag.objects.filter(blog=blog, pk=num).first()
        if tag:
            return render(request, 'site_detail.html', {'tag': tag, 'user': user})
        else:
            return render(request, 'error.html')
    else:
        archive = models.Article.objects.filter(blog=blog).annotate(month=TruncMonth('upload_time')).filter(
            month=datetime.datetime(int(num[0:4]), int(num[-2:]), 1, 0, 0, 0))
        if archive:
            return render(request, 'site_detail.html', {'archive': archive, 'user': user})
        return render(request, 'error.html')


def site(request, username):
    user = models.UserInfo.objects.get(username=username)
    if not user:
        return render(request, 'error.html')
    article = models.Article.objects.filter(blog__userinfo__username=username)
    return render(request, 'personal_site.html', locals())


def article_detail(request, username, article_id):
    user = models.UserInfo.objects.get(username=username)
    article = models.Article.objects.filter(blog__userinfo__username=username, pk=article_id)
    like = models.LikeAndAgainst.objects.filter(article=article, like=1)
    against = models.LikeAndAgainst.objects.filter(article=article, against=1)
    if not article:
        return render(request, 'error.html')
    root_comments = models.Comment.objects.filter(article=article, floor__gt=0)
    sub_comments = models.Comment.objects.filter(article=article, parent_floor_id__gt=0)
    outer_list = []
    for root in root_comments:
        inner_list = []
        dic = {}
        for sub in sub_comments:
            if sub.parent_floor_id == root.id:
                inner_list.append(sub)
        dic[root] = inner_list
        outer_list.append(dic)
    comment_page = request.GET.get('page')
    if not comment_page:
        comment_page = 1
    paginator = Paginator(outer_list, 3)
    pages = paginator.page(comment_page)
    page_range = paginator.page_range
    return render(request, 'article_detail.html', locals())


def like_and_against(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'msg': '请先登录'})
    article_id = request.POST.get('article')
    if models.LikeAndAgainst.objects.filter(article=article_id, user=request.user):
        return JsonResponse({'status': 'error', 'msg': '已经投过票'})
    vote = request.POST.get('vote')
    if vote == 'like':
        with transaction.atomic():
            models.LikeAndAgainst.objects.create(like=True, article_id=int(article_id), user=request.user)
            models.Article.objects.filter(pk=int(article_id)).update(like_count=F('like_count') + 1)
    else:
        models.LikeAndAgainst.objects.create(against=True, article_id=int(article_id), user=request.user)
    return JsonResponse({'status': 'success', 'vote': vote})


def comment(request, where):
    if request.is_ajax():
        user = request.user
        if where == 'reply_floor':
            content = request.POST.get('comment')
            parent_floor = request.POST.get('floor')
            article_id = request.POST.get('article_id')
            parent_floor_id = models.Comment.objects.get(article_id=article_id, floor=parent_floor).id
            obj = models.Comment.objects.create(content=content, article_id=int(article_id), user=user,
                                                parent_floor_id=parent_floor_id)
            time = obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
            models.Article.objects.filter(pk=article_id).update(comment_count=F('comment_count') + 1)
            return JsonResponse({'status': 'success', 'time': time, 'content': obj.content})
        elif where == 'reply_user':
            content = request.POST.get('comment')
            parent_floor = request.POST.get('floor')
            article_id = request.POST.get('article_id')
            to_username = content.split(' ')[1]
            reply_to = models.UserInfo.objects.get(username=to_username)
            if not reply_to:
                return JsonResponse({'status': 'error', 'msg': '未知错误'})
            content = content.replace('回复 ' + to_username + ' :', '')
            parent_floor_id = models.Comment.objects.get(article_id=article_id, floor=parent_floor).id
            obj = models.Comment.objects.create(content=content, article_id=int(article_id), user=user,
                                                parent_floor_id=parent_floor_id, reply=reply_to)
            time = obj.create_time.strftime('%Y-%m-%d %H:%M:%S')
            models.Article.objects.filter(pk=article_id).update(comment_count=F('comment_count') + 1)
            return JsonResponse(
                {'status': 'success', 'time': time, 'content': obj.content, 'to_user': obj.reply.username})
        else:
            content = request.POST.get('comment')
            root_floor = int(request.POST.get('floor')) + 1
            article_id = request.POST.get('article_id')
            models.Comment.objects.create(content=content, article_id=int(article_id), user=user, floor=root_floor)
            models.Article.objects.filter(pk=article_id).update(root_floor_count=F('root_floor_count') + 1,
                                                                comment_count=F('comment_count') + 1)
            return JsonResponse({'status': 'success'})


def timmer(func):
    def inner(*args,**kwargs):
        res = func(*args,**kwargs)
        return res
    return inner