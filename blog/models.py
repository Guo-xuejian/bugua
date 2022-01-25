from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from django.db import models
from markdown import markdown


# 日志表
class Log(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=64, verbose_name='访问IP', help_text='访问用户的IP地址')
    time = models.DateTimeField(auto_now_add=True, verbose_name='访问时间', help_text='该用户的访问时刻')
    url = models.CharField(max_length=64, verbose_name='访问的URL', help_text='该用户访问的URL地址')
    device = models.CharField(max_length=256, null=True, verbose_name='访问的浏览器', help_text='该用户是用什么浏览器访问的')
    platform = models.CharField(max_length=256, null=True, verbose_name='访问的系统', help_text='该用户用的是什么操作系统')

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['id']
        verbose_name_plural = '日志'


# 用户表
class UserInfo(AbstractUser):
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.png', verbose_name='头像', help_text='该用户的头像')
    bg_img = models.FileField(upload_to='bg_img/', default='bg_img/default_bg.jpg', verbose_name='头像',
                              help_text='该用户的主页背景')
    province = models.CharField(max_length=32, default='', verbose_name='省', help_text='该用户的省')
    city = models.CharField(max_length=32, default='', verbose_name='城市', help_text='该用户的市')
    gender = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')), default=0, verbose_name='性别',
                                 help_text='该用户的性别')
    phone = models.CharField(max_length=11, null=True, default='', verbose_name='联系方式', help_text='该用户的联系方式')
    blog = models.OneToOneField(to='Blog', on_delete=models.CASCADE, null=True, verbose_name='博客', help_text='该用户的博客',
                                related_name='Blog')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户'


# 博客表（个人站点）
class Blog(models.Model):
    title = models.CharField(max_length=32, verbose_name='博主昵称', help_text='博主昵称')
    subtitle = models.CharField(max_length=32, verbose_name='子标题/公告', help_text='博客的子标题/公告')
    style = models.CharField(max_length=32, verbose_name='样式', help_text='该博客独有的样式')  # 此处未启用
    # publisher = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='作者', related_name='Userinfo',
    #                          help_text='该文章属于哪个作者')
    # userinfo = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE, null=True, verbose_name='个人信息',
    #                                 help_text='该博客对应的个人站点')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '博客站点'


# 文章表
class Article(models.Model):
    title = models.CharField(max_length=32, verbose_name='标题', help_text='文章的标题')
    head_img = models.FileField(upload_to='article_head_img/', default='article_head_img/default_head.png',
                                verbose_name='头图',
                                help_text='文章的头图')
    description = models.CharField(max_length=128, verbose_name='摘要', help_text='简要描述该文章')
    content = models.TextField(verbose_name='内容', help_text='文章的内容')
    markdown = models.TextField(verbose_name='Markdown内容', default='暂无', help_text='文章的Markdown内容')
    area = models.CharField(verbose_name='文章所属专区', choices=((0, '问答'), (1, '休闲'), (2, '原创')), max_length=64,
                            default='', help_text='该文章所属的专区')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='该文章的创建时间')

    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间', help_text='该文章的最后修改时间')
    up_num = models.IntegerField(default=0, verbose_name='点赞数', help_text='该文章的点赞数')
    down_num = models.IntegerField(default=0, verbose_name='点踩数', help_text='该文章的点踩数')
    comment_num = models.IntegerField(default=0, verbose_name='评论数', help_text='该文章的评论数')
    blog = models.ForeignKey(to='Blog', on_delete=models.CASCADE, null=True, blank=True, verbose_name='博客',
                             help_text='该文章属于哪个博客页面')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='分类',
                                 help_text='该文章属于哪个分类')
    tag = models.ManyToManyField(to='Tag', through='Tag2Article',
                                 through_fields=('article', 'tag'), verbose_name='标签',
                                 help_text='该文章有哪些标签')

    def get_text_md(self):
        return mark_safe(markdown(self.content))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'
        ordering = ['id', ]


# 标签表
class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='标签', help_text='标签的名字')
    blog = models.ForeignKey(to='Blog', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='博客',
                             help_text='该标签属于哪个博客页面')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '标签'


# 分类表
class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='分类', help_text='分类的名称')
    blog = models.ForeignKey(to='Blog', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='博客',
                             help_text='该分类属于哪个博客页面')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '分类'


# 评论表
class Comment(models.Model):
    user = models.ForeignKey(to='UserInfo', on_delete=models.DO_NOTHING, verbose_name='用户', help_text='该评论来自哪个用户')
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, null=True, verbose_name='文章',
                                help_text='评论的对象是哪篇文章')
    content = models.CharField(max_length=256, verbose_name='内容', help_text='评论的内容')
    comment_time = models.DateTimeField(auto_now_add=True, verbose_name='时间', help_text='评论的时间')
    comment_id = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, verbose_name='评论id',
                                   help_text='对哪个id的评论进行评论')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论'


# 点赞点踩
class UpAndDown(models.Model):
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, verbose_name='用户', help_text='来自哪个用户')
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, null=True, verbose_name='文章',
                                help_text='针对哪篇文章')
    is_up = models.BooleanField(null=True, verbose_name='点赞点踩', help_text='True为点赞，False为点踩')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='点赞点踩的时间')

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = '点赞点踩'


# 标签、文章关联表
class Tag2Article(models.Model):
    tag = models.ForeignKey(to='Tag', on_delete=models.SET_DEFAULT, default='', verbose_name='标签', help_text='关联的标签')
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, default='', verbose_name='文章',
                                help_text='关联的文章')

    class Meta:
        verbose_name_plural = '标签关联文章'


# 轮播图表
class Swiper(models.Model):
    image = models.FileField(upload_to='swiper_img/', default='swiper_img/default.jpg', verbose_name='图片',
                             help_text='轮播图的图片')
    title = models.CharField(max_length=32, verbose_name='标题', help_text='图片的标题')
    img_url = models.CharField(max_length=64, verbose_name='URL', help_text='点击图片要跳转的URL地址')

    def __str__(self):
        return self.img_url

    class Meta:
        verbose_name_plural = '轮播图'
