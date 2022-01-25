from .simpleui import *
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '8gu&2ob2mhh=h##ed@54%)qbqc^f8!jx#*d^r4-axs#n04(kvy'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "simpleui",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'markdown',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blog.x_middleware.PlatformMiddleware',
]

ROOT_URLCONF = 'bugua.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bugua.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "bugua",  # 数据库名
        "HOST": "127.0.0.1",  # 主机IP（本地为127.0.0.1）
        "PORT": "3306",  # 端口号：默认3306
        "USER": "root",  # 数据库用户名
        "PASSWORD": "root",  # 数据库密码
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'  # 设置语言为中文

TIME_ZONE = 'Asia/Shanghai'  # 设置时区为亚洲上海

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 禁用UTC时间

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

STATIC_ROOT = os.path.join(BASE_DIR, "collectstatic")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'blog.UserInfo'

# Markdown相关配置
MDEDITOR_CONFIGS = {
    'default': {
        'width': '90% ',  # Custom edit box width  宽度，整个页面的百分之多少
        'heigth': 500,  # Custom edit box height   高度，单位为px
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime"
                                                                                                           "emoji",
                    "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar   工具栏
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
        # image upload format type  允许上传的图片 的格式，不在这个里面的格式将不允许被上传
        'image_floder': 'editor',  # image save the folder name   上传图片后存放的目录，BASE_DIR/MEDIA_ROOT/editor
        'theme': 'dark',  # edit box theme, dark / default  mdeditor主题，dark/default两种
        'preview_theme': 'default',  # Preview area theme, dark / default  内容显示区主题 dark/default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default   文本编辑区主题  pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement  是否打开搜索替换
        'emoji': True,  # whether to open the expression function  是否允许使用emoji表情
        'tex': True,  # whether to open the tex chart function   是否打开tex图表功能
        'flow_chart': True,  # whether to open the flow chart function   是否打开流程图功能
        'sequence': True  # Whether to open the sequence diagram function   是否打开序列图函数
    }
}
