from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import transaction
from django.contrib import auth
from django.urls import reverse
from django.db.models import F
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from blog import x_forms
from blog import models
from io import BytesIO

import markdown
import datetime
import random
import json
import time
import uuid
import re


# 未启用
class CommonResponse:
    def __init__(self):
        self.code = 100

    @property
    def all(self):
        return self.__dict__


# 退出
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


# 注册
def register(request):
    if request.method == 'GET':
        form = x_forms.FormRegister()
        return render(request, 'Register.html', context={'form': form})
    elif request.method == 'POST':
        form = x_forms.FormRegister(data=request.POST)
        res = {'code': '', 'msg': ''}
        if form.is_valid():
            data = form.cleaned_data
            data.pop('re_password')
            file = request.FILES.get('avatar')
            if file:
                data['avatar'] = file
            models.UserInfo.objects.create_user(**data)
            res['code'] = 100
            res['msg'] = '注册成功！'
            res['url'] = '/login/'
            return JsonResponse(res)
        else:
            res['code'] = 101
            res['msg'] = '数据校验失败！'
            res['err'] = form.errors
            return JsonResponse(res)
    else:
        return HttpResponse('非法请求！')


# 校验用户名是否存在
def check_username(request):
    if request.method == 'GET':
        res = {'code': 101, 'msg': '该用户名已存在'}
        username = request.GET.get('username')
        if username:
            user = models.UserInfo.objects.filter(username=username).count()
            if not user:
                res['code'] = 100
            return JsonResponse(res)
        else:
            res['code'] = 102
            res['msg'] = '用户名不能为空'
            return JsonResponse(res)
    else:
        return HttpResponse('非法请求！')


# 登录
def login(request):
    if request.method == 'POST':
        res = {'code': 100}
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        if request.session.get('valid_code').upper() == valid_code.upper() or valid_code == '123':
            user = auth.authenticate(username=username, password=password)
            freezed = models.UserInfo.objects.filter(username=username, is_active=0).first()
            res['url'] = '/index/'
            if freezed:
                res['code'] = 105
                res['msg'] = '账户被冻结'
            if user:
                auth.login(request, user)
                res['msg'] = '登录成功'
            else:
                res['code'] = 101
                res['msg'] = '用户名密码错误'
        else:
            res['code'] = 102
            res['msg'] = '验证码错误'
        return JsonResponse(res)
    elif request.method == 'GET':
        form = x_forms.FormLogin()
        return render(request, 'Login.html', {'form': form})
    else:
        return HttpResponse('非法请求！')


# 获取随机颜色
def get_rgb():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# 获取验证码
def get_valid_code(request):
    img = Image.new('RGB', (200, 38), get_rgb())
    img_draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype('./static/font/FZFenSTXJW.TTF', 25)
    valid_code = ''
    for i in range(5):
        low_char = chr(random.randint(97, 122))
        num_char = random.randint(0, 9)
        upper_char = chr(random.randint(65, 90))
        res = random.choice([low_char, num_char, upper_char])
        valid_code += str(res)
        img_draw.text((i * 40 + 10, 5), str(res), get_rgb(), img_font)
    request.session['valid_code'] = valid_code
    print(valid_code)

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    return HttpResponse(data)


# 查看所有用户
def user_info(request):
    if request.method == 'GET':
        info = models.UserInfo.objects.all()
        return render(request, 'other/UserInfo.html', {'info': info})


# 上传轮播图
def upload_swiper(request):
    if request.method == 'POST':
        file = request.FILES.get('swiper_img')
        url = request.POST.get('url')
        title = request.POST.get('title')
        models.Swiper.objects.create(image=file, img_url=url, title=title)
        return redirect(reverse('upload_swiper'))
    elif request.method == 'GET':
        swiper_list = models.Swiper.objects.all()
        return render(request, 'other/UploadSwiper.html', {'swiper_list': swiper_list})


# 错误404页面
def error(request):
    return render(request, 'other/Error.html')


# 主页
def index(request):
    swiper_list = models.Swiper.objects.all()
    article_list = models.Article.objects.filter(area=0).order_by('-create_time')
    page_num_int = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, 6)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    start = 1
    end = paginator.num_pages
    if page_num_int > int(end):
        return redirect(reverse('error'))
    return render(request, 'Index.html', locals())


# 休闲专区
def les_area(request):
    swiper_list = models.Swiper.objects.all()
    article_list = models.Article.objects.filter(area=1).order_by('-create_time')
    page_num_int = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, 6)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    start = 1
    end = paginator.num_pages
    if page_num_int > int(end):
        return redirect(reverse('error'))
    return render(request, 'Leisure_area.html', locals())


# 原创专区
def orn_area(request):
    swiper_list = models.Swiper.objects.all()
    article_list = models.Article.objects.filter(area=2).order_by('-create_time')
    page_num_int = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, 6)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    start = 1
    end = paginator.num_pages
    if page_num_int > int(end):
        return redirect(reverse('error'))
    return render(request, 'Original_area.html', locals())


# 个人站点
def site(request, name, **kwargs):
    user = models.UserInfo.objects.filter(username=name).first()
    if user:
        try:
            article_list = user.blog.article_set.all()
            query = kwargs.get('query', None)
            if query == 'category':
                condition = kwargs.get('condition')
                article_list = article_list.filter(category_id=condition)
            elif query == 'tag':
                condition = kwargs.get('condition')
                article_list = article_list.filter(tag__id=condition)
            elif query == 'archive':
                condition = kwargs.get('condition')
                year, month = condition.split('/')
                article_list = article_list.filter(create_time__year=year, create_time__month=month)
            return render(request, 'site.html', locals())
        except:
            return render(request, 'other/Error.html')
    else:
        return render(request, 'other/Error.html')


# 文章详情
def article_detail(request, name, id):
    user = models.UserInfo.objects.get(username=name)
    article = models.Article.objects.get(id=id)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    content = md.convert(article.markdown)
    # toc = md.toc
    # article.toc = article.markdown.toc
    n = content.count('<div class="codehilite">', 0, len(content))
    for i in range(n):
        content = re.sub(r'<div class="codehilite">',
                         '<button id="ecodecopy" class="copybtn btn btn-outline-light btn-sm" '
                         'data-clipboard-action="copy" '
                         'data-clipboard-target="#code{}">复制</button> '
                         '<div class="codehilite" id="code{}">'.format(i, i), content, 1)
    comment_list = models.Comment.objects.filter(article=article)
    return render(request, 'article/Article_Detail.html', locals())


# 点赞点踩
@login_required(login_url='/login/')
def upanddown(request):
    res = {'code': 100, 'msg': ''}
    if request.user.is_authenticated:
        article_id = request.POST.get('article_id')
        user_id = request.user.id
        is_up = json.loads(request.POST.get('is_up'))
        article_obj = models.Article.objects.filter(pk=article_id).first()
        clicked = models.UpAndDown.objects.filter(article_id=article_id, user_id=user_id).first()
        if not request.user == article_obj.blog.Blog:
            if clicked:
                res['code'] = 101
                res['msg'] = '您已经支持过' if clicked.is_up else '您已经反对过'
            else:
                with transaction.atomic():
                    models.UpAndDown.objects.create(article_id=article_id, user_id=user_id, is_up=is_up)
                    if is_up:
                        models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                        res['msg'] = '点赞成功'
                    else:
                        models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                        res['msg'] = '点踩成功'
        else:
            res['code'] = 103
            res['msg'] = '不能推荐自己的内容' if is_up else '不能反对自己的内容'
    else:
        res['code'] = 104
        res['msg'] = '请先<a href="/login/">登录</a>'
    return JsonResponse(res)


# 文章评论
@login_required(login_url='/login/')
def comment(request):
    res = {'code': 100, 'msg': ''}
    if request.is_ajax():
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        parent = request.POST.get('parent')
        if request.user.is_authenticated:
            article = models.Comment.objects.create(user=request.user, article_id=article_id, content=content,
                                                    comment_id_id=parent)
            models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
            res['msg'] = '评论成功'
            res['username'] = article.user.username
            res['content'] = article.content
            if parent:
                res['parent_name'] = article.comment_id.user.username
        else:
            res['code'] = 109
            res['msg'] = '请先登录'

    return JsonResponse(res)


# 后台管理
def backend(request):
    article_num = models.Article.objects.filter(blog=request.user.blog).count()
    article_num = models.Article.objects.filter(blog=request.user.blog).count()
    category_num = models.Category.objects.filter(blog=request.user.blog).count()
    tag_num = models.Tag.objects.filter(blog=request.user.blog).count()
    article_list = models.Article.objects.filter(blog=request.user.blog)
    page_num_int = int(request.GET.get('page', 1))
    paginator = Paginator(article_list, 10)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    category_list = models.Category.objects.filter(blog=request.user.blog)
    tag_list = models.Tag.objects.filter(blog=request.user.blog)
    start = 1
    end = paginator.num_pages
    blog = request.user.blog
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    return render(request, 'user/Backend.html', locals())


# 文章添加
@login_required(login_url='/login/')
def add_article(request):
    res = {'code': 100, 'msg': '发布成功'}
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('html_doc')
        markdown = request.POST.get('mark_doc')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        area = request.POST.get('area')
        head_img = request.FILES.get('head_img')
        tags1 = tags.split(',')
        soup = BeautifulSoup(content, 'html.parser')
        description = soup.text[0:120]
        res_script = soup.find_all('script')
        for script in res_script:
            script.decompose()
        article = models.Article.objects.create(
            title=title,
            blog=request.user.blog,
            description=description,
            content=str(soup),
            markdown=markdown,
            category_id=category,
            area=area,
            head_img=head_img
        )
        ll = []
        for tag in tags1:
            ll.append(models.Tag2Article(article_id=article.pk, tag_id=tag))
        models.Tag2Article.objects.bulk_create(ll)
        return JsonResponse(res)
    return render(request, 'user/Backend.html', locals())


# 文章更新
@login_required(login_url='/login/')
def update_article(request, uid):
    blog = request.user.blog
    if request.method == 'POST':
        res = {'code': 100, 'msg': '修改成功'}
        title = request.POST.get('title')
        content = request.POST.get('html_doc')
        markdown = request.POST.get('mark_doc')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        area = request.POST.get('area')
        head_img = request.FILES.get('head_img')
        modify_time = datetime.datetime.now()
        if not tags:
            res['code'] = 200
            res['msg'] = '请选择文章标签'
        if not head_img:
            res['code'] = 200
            res['msg'] = '请选择图片'
            return JsonResponse(res)
        new_head_img = 'article_head_img/' + head_img.name
        img = Image.open(head_img)
        img.save('media/article_head_img/' + head_img.name)
        tags1 = tags.split(',')
        soup = BeautifulSoup(content, 'html.parser')
        description = soup.text[0:120]
        res_script = soup.find_all('script')
        for script in res_script:
            script.decompose()
        models.Article.objects.filter(pk=uid, blog=blog).update(
            title=title,
            blog=request.user.blog,
            description=description,
            content=str(soup),
            markdown=markdown,
            category_id=category,
            area=area,
            head_img=new_head_img,
            modify_time=modify_time
        )
        models.Tag2Article.objects.filter(article__id=uid).delete()
        article_obj_list = []
        ll = []
        for i in tags1:
            tag_article_obj = models.Tag2Article(article_id=uid, tag_id=i)
            article_obj_list.append(tag_article_obj)
        models.Tag2Article.objects.bulk_create(article_obj_list)
        return JsonResponse(res)
    article_obj = models.Article.objects.filter(pk=uid).first()
    category_list = models.Category.objects.filter(blog=blog)
    tag_list = models.Tag.objects.filter(blog=blog)
    return render(request, 'article/Update_Article.html', locals())


# 添加分类、标签
@login_required(login_url='/login/')
def add_target(request, target):
    res = {'code': 100, 'msg': '创建成功'}
    if target == 'category':
        name = request.POST.get('name')
        obj = models.Category.objects.filter(name=name, blog=request.user.blog).first()
        if not obj:
            models.Category.objects.create(name=name, blog=request.user.blog)
        else:
            res['code'] = 200
            res['msg'] = '该分类已存在'
    elif target == 'tag':
        name = request.POST.get('name')
        obj = models.Tag.objects.filter(name=name, blog=request.user.blog).first()
        if not obj:
            models.Tag.objects.create(name=name, blog=request.user.blog)
        else:
            res['code'] = 200
            res['msg'] = '该标签已存在'
    return JsonResponse(res)


# 标签、分类更新
@login_required(login_url='/login/')
def update_target(request, target, uid):
    if request.method == 'POST':
        res = {'code': 100}
        name = request.POST.get('name')
        if target == 'category':
            obj = models.Category.objects.filter(id=uid, name=name).first()
            if not obj:
                models.Category.objects.filter(id=uid).update(name=name)
                res['msg'] = '修改成功'
            else:
                res['code'] = 200
                res['msg'] = '该分类已存在'
        elif target == 'tag':
            obj = models.Tag.objects.filter(id=uid, name=name).first()
            if not obj:
                models.Tag.objects.filter(id=uid).update(name=name)
                res['msg'] = '修改成功'
            else:
                res['code'] = 200
                res['msg'] = '该标签已存在'
        return JsonResponse(res)


# 标签、分类的删除
@login_required(login_url='/login/')
def delete_target(request, target, did):
    if request.method == 'POST':
        res = {'code': 100}
        if target == 'article':
            models.Article.objects.filter(id=did).delete()
        elif target == 'category':
            models.Category.objects.filter(id=did).delete()
        elif target == 'tag':
            models.Tag2Article.objects.filter(tag_id=did).delete()
            models.Tag.objects.filter(id=did).delete()
        return JsonResponse(res)


# Markdown编辑器上传图片
@login_required(login_url='/login/')
def upload_img(request):
    img_obj = request.FILES.get('editormd-image-file')
    img = Image.open(img_obj)
    uid = ''.join(str(uuid.uuid4()).split('-'))[::4]
    tmp = img_obj.name.rsplit('.', 1)[-1]
    t = str(time.time()).split('.')
    img_name = ''.join([t[0], t[-1], '_', uid, '.', tmp])
    img.save('media/article_img/' + img_name)
    return JsonResponse({'success': 1, 'msg': '上传成功', 'url': f"/media/article_img/{img_name}"})


# 修改个人信息
@login_required(login_url='/login/')
def set_info(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        province = request.POST.get("province")
        city = request.POST.get("city")
        models.UserInfo.objects.filter(username=request.user.username).update(phone=phone, email=email,
                                                                              province=province, city=city,
                                                                              gender=gender)
        return redirect(reverse('set_info'))
    return render(request, 'user/Set_Info.html')


# 创建个人站点
@login_required(login_url='/login/')
def create_site(request):
    if request.is_ajax():
        res = {'code': 100, 'msg': ''}
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        obj = models.UserInfo.objects.filter(username=request.user.username).first()
        blog = obj.blog
        if blog:
            blog.title = title
            blog.subtitle = subtitle
            blog.save()
            res['msg'] = '个人空间修改成功'
        else:
            is_exist = models.Blog.objects.filter(title=title).first()
            if not is_exist:
                blog = models.Blog.objects.create(title=title, subtitle=subtitle)
                obj.blog = blog
                obj.save()
                res['msg'] = '个人空间创建成功'
            else:
                res['code'] = 200
                res['msg'] = '该空间名已存在'
        return JsonResponse(res)


# 修改密码
@login_required(login_url='/login/')
def change_password(request):
    data = {'code': 100, 'msg': '修改成功'}
    if request.method == 'POST':
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        if request.user.check_password(old_pwd):
            if old_pwd == new_pwd:
                data['code'] = 101
                data['msg'] = '新密码与旧密码不能相同'
            else:
                request.user.set_password(new_pwd)
                request.user.save()
        else:
            data['code'] = 102
            data['msg'] = '旧密码错误，请重试'
        return JsonResponse(data)


# 修改头像
@login_required(login_url='/login/')
def change_avatar(request):
    if request.method == 'POST':
        data = {'code': 100, 'msg': ''}
        img_obj = request.FILES.get('avatar')
        if img_obj:
            url = 'avatar/' + img_obj.name
            img = Image.open(img_obj)
            img.save('media/avatar/' + img_obj.name)
            models.UserInfo.objects.filter(username=request.user.username).update(avatar=url)
            data['msg'] = '头像修改成功'
        else:
            data['code'] = 200
            data['msg'] = '请上传头像'
        return JsonResponse(data)


# 修改背景
@login_required(login_url='/login/')
def change_bg(request):
    if request.method == 'POST':
        data = {'code': 100, 'msg': ''}
        img_obj = request.FILES.get('bg_img')
        if img_obj:
            url = 'bg_img/' + img_obj.name
            img = Image.open(img_obj)
            img.save('media/bg_img/' + img_obj.name)
            models.UserInfo.objects.filter(username=request.user.username).update(bg_img=url)
            data['msg'] = '背景修改成功'
        else:
            data['code'] = 200
            data['msg'] = '请选择背景'
        return JsonResponse(data)


# 记录日志+分页
def log(request):
    log_num = models.Log.objects.count()
    page_num_int = int(request.GET.get('page', 1))
    log_list = models.Log.objects.all()
    paginator = Paginator(log_list, 10)
    if paginator.num_pages > 9:
        if page_num_int - 4 < 1:
            page_range = range(1, 9)
        elif page_num_int + 4 > paginator.num_pages:
            page_range = range(paginator.num_pages - 8, paginator.num_pages + 1)
        else:
            page_range = range(page_num_int - 4, page_num_int + 4)
    else:
        page_range = paginator.page_range
    page = paginator.page(page_num_int)
    return render(request, 'other/Log.html',
                  {'page_range': page_range, 'page': page, 'page_num_int': page_num_int, 'log_num': log_num, 'start': 1,
                   'end': paginator.num_pages})


# 禁用账户
def disable_account(request):
    disable_id = request.GET.get('disable_id')
    models.UserInfo.objects.filter(id=disable_id).update(is_active=0)
    return redirect(reverse('user_info'))


# 启用账户
def able_account(request):
    able_id = request.GET.get('able_id')
    models.UserInfo.objects.filter(id=able_id).update(is_active=1)
    return redirect(reverse('user_info'))


# 设置为超级用户
def super_account(request):
    super_id = request.GET.get('super_id')
    models.UserInfo.objects.filter(id=super_id).update(is_superuser=1)
    return redirect(reverse('user_info'))


# 联系我们
def contact(request):
    return render(request, 'Contact.html')