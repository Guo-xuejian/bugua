# Generated by Django 2.2.2 on 2022-01-25 15:45

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.FileField(default='avatar/default.png', help_text='??????????????????', upload_to='avatar/', verbose_name='??????')),
                ('bg_img', models.FileField(default='bg_img/default_bg.jpg', help_text='????????????????????????', upload_to='bg_img/', verbose_name='??????')),
                ('province', models.CharField(default='', help_text='???????????????', max_length=32, verbose_name='???')),
                ('city', models.CharField(default='', help_text='???????????????', max_length=32, verbose_name='??????')),
                ('gender', models.IntegerField(choices=[(0, '??????'), (1, '???'), (2, '???')], default=0, help_text='??????????????????', verbose_name='??????')),
                ('phone', models.CharField(default='', help_text='????????????????????????', max_length=11, null=True, verbose_name='????????????')),
            ],
            options={
                'verbose_name_plural': '??????',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='???????????????', max_length=32, verbose_name='??????')),
                ('head_img', models.FileField(default='article_head_img/default_head.png', help_text='???????????????', upload_to='article_head_img/', verbose_name='??????')),
                ('description', models.CharField(help_text='?????????????????????', max_length=128, verbose_name='??????')),
                ('content', models.TextField(help_text='???????????????', verbose_name='??????')),
                ('markdown', models.TextField(default='??????', help_text='?????????Markdown??????', verbose_name='Markdown??????')),
                ('area', models.CharField(choices=[(0, '??????'), (1, '??????'), (2, '??????')], default='', help_text='????????????????????????', max_length=64, verbose_name='??????????????????')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='????????????????????????', verbose_name='????????????')),
                ('modify_time', models.DateTimeField(auto_now=True, help_text='??????????????????????????????', verbose_name='????????????')),
                ('up_num', models.IntegerField(default=0, help_text='?????????????????????', verbose_name='?????????')),
                ('down_num', models.IntegerField(default=0, help_text='?????????????????????', verbose_name='?????????')),
                ('comment_num', models.IntegerField(default=0, help_text='?????????????????????', verbose_name='?????????')),
            ],
            options={
                'verbose_name_plural': '??????',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='????????????', max_length=32, verbose_name='????????????')),
                ('subtitle', models.CharField(help_text='??????????????????/??????', max_length=32, verbose_name='?????????/??????')),
                ('style', models.CharField(help_text='????????????????????????', max_length=32, verbose_name='??????')),
            ],
            options={
                'verbose_name_plural': '????????????',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip', models.CharField(help_text='???????????????IP??????', max_length=64, verbose_name='??????IP')),
                ('time', models.DateTimeField(auto_now_add=True, help_text='????????????????????????', verbose_name='????????????')),
                ('url', models.CharField(help_text='??????????????????URL??????', max_length=64, verbose_name='?????????URL')),
                ('device', models.CharField(help_text='???????????????????????????????????????', max_length=256, null=True, verbose_name='??????????????????')),
                ('platform', models.CharField(help_text='????????????????????????????????????', max_length=256, null=True, verbose_name='???????????????')),
            ],
            options={
                'verbose_name_plural': '??????',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Swiper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(default='swiper_img/default.jpg', help_text='??????????????????', upload_to='swiper_img/', verbose_name='??????')),
                ('title', models.CharField(help_text='???????????????', max_length=32, verbose_name='??????')),
                ('img_url', models.CharField(help_text='????????????????????????URL??????', max_length=64, verbose_name='URL')),
            ],
            options={
                'verbose_name_plural': '?????????',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='???????????????', max_length=32, verbose_name='??????')),
                ('blog', models.ForeignKey(blank=True, help_text='?????????????????????????????????', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog', verbose_name='??????')),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='UpAndDown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_up', models.BooleanField(help_text='True????????????False?????????', null=True, verbose_name='????????????')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='?????????????????????', verbose_name='????????????')),
                ('article', models.ForeignKey(help_text='??????????????????', null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='??????')),
                ('user', models.ForeignKey(help_text='??????????????????', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='??????')),
            ],
            options={
                'verbose_name_plural': '????????????',
            },
        ),
        migrations.CreateModel(
            name='Tag2Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(default='', help_text='???????????????', on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='??????')),
                ('tag', models.ForeignKey(default='', help_text='???????????????', on_delete=django.db.models.deletion.SET_DEFAULT, to='blog.Tag', verbose_name='??????')),
            ],
            options={
                'verbose_name_plural': '??????????????????',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(help_text='???????????????', max_length=256, verbose_name='??????')),
                ('comment_time', models.DateTimeField(auto_now_add=True, help_text='???????????????', verbose_name='??????')),
                ('article', models.ForeignKey(help_text='??????????????????????????????', null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='??????')),
                ('comment_id', models.ForeignKey(help_text='?????????id?????????????????????', null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='??????id')),
                ('user', models.ForeignKey(help_text='???????????????????????????', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='??????')),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='???????????????', max_length=32, verbose_name='??????')),
                ('blog', models.ForeignKey(blank=True, help_text='?????????????????????????????????', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog', verbose_name='??????')),
            ],
            options={
                'verbose_name_plural': '??????',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(blank=True, help_text='?????????????????????????????????', null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog', verbose_name='??????'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, help_text='???????????????????????????', null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='??????'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(help_text='????????????????????????', through='blog.Tag2Article', to='blog.Tag', verbose_name='??????'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(help_text='??????????????????', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Blog', to='blog.Blog', verbose_name='??????'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
