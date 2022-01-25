from django.urls import path, re_path, include
from django.views.static import serve
from django.contrib import admin
from django.conf import settings
from blog import views

urlpatterns = [
    path('', views.index, name='index'),  # 默认直接进入index主页
    path('able_account/', views.able_account, name='able_account'),  # 启用账户
    path('add_article/', views.add_article, name='add_article'),  # 添加文章
    path('admin/', admin.site.urls),  # Django默认的admin后台管理
    path('backend/', views.backend, name='backend'),  # 自定义后台管理
    path('change_avatar/', views.change_avatar, name='change_avatar'),  # 修改头像
    path('change_bg/', views.change_bg, name='change_bg'),  # 修改首页、个人站点背景图片
    path('change_password/', views.change_password, name='change_password'),  # 修改密码
    path('check_username/', views.check_username, name='check_username'),  # 校验用户名是否存在
    path('comment/', views.comment, name='comment'),  # 评论
    path('create_site/', views.create_site, name='create_site'),  # 创建个人站点
    path('contact', views.contact, name='contact'),  #联系我们
    path('disable_account/', views.disable_account, name='disable_account'),  # 禁用账户
    path('error/', views.error, name='error'),  # 404页面
    path('get_valid_code/', views.get_valid_code, name='get_valid'),  # 获取验证码
    path('index/', views.index, name='index'),  # index主页
    path('leisure/', views.les_area, name='leisure'),
    path('log/', views.log, name='log'),  # 查看日志
    path('login/', views.login, name='login'),  # 登录
    path('logout/', views.logout, name='logout'),  # 注销/退出
    path('mdeditor/', include('mdeditor.urls')),  # 用了Markdown编辑器需要的路由
    path('original', views.orn_area, name='original'),
    path('register/', views.register, name='register'),  # 注册页面
    path('super_account/', views.super_account, name='super_account'),  # 设置为超级管理员
    path('set_info/', views.set_info, name='set_info'),  # 设置个人信息
    path('upanddown/', views.upanddown, name='upanddown'),  # 点赞点踩
    path('update_article/', views.update_article, name='update_article'),  # 修改文章
    path('upload_swiper/', views.upload_swiper, name='upload_swiper'),  # 上传轮播图
    path('upload_img/', views.upload_img, name='upload_img'),  # 上传Markdown文本编辑器内的图片
    path('user_info/', views.user_info, name='user_info'),  # 查看、管理所有用户
    re_path('^(?P<name>\w+)$', views.site, name='sites'),  # 个人站点
    re_path('^(?P<name>\w+)/(?P<query>category|tag|archive)/(?P<condition>.*).html$', views.site),  # 个人站点的侧边栏过滤
    re_path('^(?P<name>\w+)/article/(?P<id>\d+).html$', views.article_detail),  # 文章详情页
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 媒体资源暴露
    re_path('add/(?P<target>\w+)', views.add_target),  # 标签、分类的更新
    re_path('delete/(?P<target>\w+)/(?P<did>\d+)', views.delete_target),  # 文章、标签、分类的删除
    re_path('update/(?P<target>\w+)/(?P<uid>\d+)', views.update_target),  # 标签、分类的更新
    re_path('update_article/(?P<uid>\d+)', views.update_article),  # 文章更新
]
