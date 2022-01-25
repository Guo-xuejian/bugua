## 一：项目介绍

### 简介

- 多人博客（多用户，每个用户可以有自己的个人站点，编写自己的博客）
- 登录注册（登录有图片验证码，注册可以上传用户自定义头像）
- 登录注册用form组件进行校验和渲染页面，Ajax提交请求
- 每个用户都有个人站点（可以根据时间、分类、标签来过滤文章）
- 每个用户拥有后台管理（可以对文章、标签、分类进行增、删、改、查，新增文章使用Markdown文本编辑器，处理XSS攻击）
- 文章支持Markdown的代码语法高亮，支持一键复制
- 每个用户可以设置个人信息，修改个人站点背景、修改头像、修改密码
- 1篇文章可以有多个标签，但是只能拥有1个分类（不支持属于多个分类，但是不限制于标签）
- 在首页显示文章的用户头像、文章标题、文章摘要、发布时间、点赞数、评论数
- 每个已登录的用户都可以对文章进行点赞点踩（只能点其中1个，点后无法继续点击，无法撤销）
- 每篇文章都可以进行评论，每个评论可以有子评论（子评论也可以有子评论，以此类推）
- 管理员用户可以上传首页轮播图，可以管理用户（禁用、启用、设置为管理员、admin后台管理）

### 页面预览

#### 注册界面

- 使用了forms组件进行校验和渲染，有局部和全局钩子
- 用户名输入框失去焦点就会判断该用户名是否存在，是否合法
- 头像上传后可以实时显示已上传的头像
- 注册按钮默认禁用，只有同意协议后才能激活按钮
- 用Ajax发送请求，用JS渲染错误提示信息

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110193956961.png)

#### 登录界面

- 用户名、密码、验证码的输入框都有失去焦点就渲染错误信息事件
- 验证码和背景随机生成，使用了`pillow`模块

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110194025662.png)

#### 管理员页面

- 管理员可以上传主页的轮播图

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110194434693.png)

- 管理员可以管理全部用户（除了自己）

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110195033715.png)

- 管理员 - Django内置admin后台管理

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110195109104.png)

#### 用户

- 所有用户都可以查看访问日志
- 日志中包含了IP地址、访问URL、访问时间、访问设备、访问平台
- 加入了分页器

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110195737091.png)

- 可以设置基本信息
- 信息设置：地址栏用了JS的省市联动，前端的JS中使用模板语法渲染当前用户的地址
- 站点设置：可以创建个人博客站点（博客昵称 + 博客公告）
- 修改密码：新密码和旧密码不能相同，旧密码必须认证成功才能修改，成功后跳转至登录界面
- 修改头像：修改时可以试试显示，修改后直接刷新页面，更新头像
- 修改背景：可以修改当前页面+主页+个人博客站点的背景图片（每个用户的个人博客站点背景图都可以不同）

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110200021170.png)

#### 后台管理

- 新增文章用了`mdeditor`编辑器，支持`Markdown`语法，左边源代码，右边预览，分类单选，标签多选，文章有自己的首图

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110201153056.png)

- 文章和分类、标签的删除根据ID传值，共用一个url和视图函数
- 分类和标签的更新也共用一个url和视图函数

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110201911188.png)

- 点击文章编辑按钮后，到新的页面进行编辑，选择已关联分类和标签

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110215510689.png)

#### 主页

- 轮播图：点击可以跳转至轮播图的链接
- 展示所有文章，使用了折叠和分页，显示文章作者的头像和发布时间、点赞数、评论数

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110202112300.png)

#### 个人博客站点

- 左侧栏：根据分类、标签、日期归档进行过滤
- 右侧栏：显示博主的头像和一些信息
- 中间主内容：显示公告和文章
- 文章：显示文章头图、文章标题、发布时间、点赞数、评论数

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110204040912.png)

#### 文章详情

- 显示发布时间、修改时间、

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110213654312.png)

- 代码块支持不同编程语言的语法高亮
- 代码块显示行号
- 有一键复制功能
- 生成侧边栏目录，点击即可跳转

![](https://gitee.com/xuexianqi/img/raw/master/img/image-20201113212038522.png)

- 点赞点踩：只能点其中1个，无法撤销，1个用户对1篇文章只能点1次
- 评论：有根评论和子评论，实时渲染

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110213914297.png)

## 二：安装与运行

### 1.开发环境

Python解释器版本：3.6

Django版本：2.2

### 2.安装

##### 所有依赖都在`requirement.txt`中，直接安装即可

```python
pip install -r requirement.txt
```

### 3.配置

> 配置文件都在`settings.py`中

##### 修改数据库配置 - 用了`MySQL数据库`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog01',    # 数据库名
        'HOST': '127.0.0.1',    # 主机IP（本地为127.0.0.1）
        'PORT': 3306,   # MySQL端口号：默认3306
        'USER':  'root',  # 数据库用户名
        'PASSWORD': '123456', # 数据库密码
    }
}
```

##### 创建数据库

```python
create database blog01;
```

##### 执行迁移命令

```python
python manage.py makemigrations
python manage.py migrate
```

##### 创建超级用户

```python
python manage.py createsuperuser
```

### 4.运行

##### 启动项目

```python
python manage.py runserver
```



## 三：表结构分析

### 1.表设计

9张表：8张物理表+1张虚拟表



#### 物理表

- 用户表：`UserInfo`
- 博客表：`Blog`
- 文章表：`Article`
- 标签表：`Tag`
- 分类表：`Category`
- 评论表：`Comment`
- 点赞点踩表：`UpAndDown`
- 轮播图表：`Swiper`



#### 虚拟表

- 文章-标签 关联表：`Article2Tag`

#### 表关系图

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201110220210794.png)

### 2.表字段分析

#### 用户表：`User`（通过继承`AbstractUser`类来扩写`auth_user`）

- avatar：用户的头像
- province：用户所在的省
- city：用户所在的城市
- gender：用户的性别
- phone：用户的联系方式
- blog：用户的博客站点（外键关联博客表`Blog`）



#### 博客表：`Blog`

- title：博客标题
- subtitle：子标题
- style：博客样式



#### 文章表：`Article`

- title：文章标题
- head_img：文章头图
- description：文章摘要
- content：文章内容
- markdown：文章的Markdown源码
- create_time：文章的创建时间
- modify_time：文章的最后修改时间
- up_num：文章的点赞数
- down_num：文章的点踩数
- comment_num：文章的评论数
- blog：属于哪个博客站点（外键关联博客表`Blog`）
- category：属于哪个分类（外键关联分类表`Category`）
- tag：文章的标签（多对多关联标签表`Tag`）



#### 标签表：`Tag`

- name：标签名
- blog：属于哪个博客站点（外键关联博客表`Blog`）



#### 分类表：`Category`

- name：分类名
- blog：属于哪个博客站点（外键关联博客表`Blog`）



#### 评论表：`Comment`

- user：评论的用户（外键关联用户表`UserInfo`）
- article：该评论属于哪篇文章（外键关联文章表`Article`）
- content：评论内容
- comment_time：评论时间
- comment_id：评论的目标id（外键进行`自关联`）



#### 点赞点踩表：`UpAndDown`

- user：来自哪个用户（外键关联用户表`UserInfo`）
- article：属于哪篇文章（外键关联文章表`Article`）
- is_up：点赞还是点踩（根据bool值来判断）
- click_time：点赞/点踩时间



#### 文章-标签 关联表：`Article2Tag`

- tag：关联标签（外键关联标签表`Tag`）
- article：关联文章（外键关联文章表`Article`）



#### 轮播图表：

- image：存放轮播图
- title：跳转的介绍
- img_url：点击跳转的地址



### 3.评论表的逻辑

一篇文章可以有多个评论，评论分为2中：

- 根评论：该评论是单独的，没有其他用户回复该评论的评论（评论的对象是文章）
- 子评论：该评论是用于回复评论的，包括回复根评论和已有子评论（评论的对象是评论，一般带有`@`）

![](https://darker-x.oss-cn-hangzhou.aliyuncs.com/img/bbs/image-20201027203253468.png)

|  id  |  user  | article |                  content                   | comment_time         | comment_id |
| :--: | :----: | :-----: | :----------------------------------------: | -------------------- | :--------: |
|  1   | 猪八戒 |    1    |         大师兄，师傅被妖怪抓走了！         | 2020.10.27  19:32:05 |    null    |
|  2   |  沙僧  |    1    |         二师兄，师傅被妖怪抓走了！         | 2020.10.27  19:35:27 |    null    |
|  3   |  沙僧  |    1    |    大师兄，师傅和二师兄都被妖怪抓走了！    | 2020.10.27  20:48:06 |    null    |
|  4   | 猪八戒 |    1    | 都是俺老猪不好，没管住师傅，自己都赔进去了 | 2020.10.27  20:49:29 |     3      |
|  5   | 孙悟空 |    1    |                  纳尼？！                  | 2020.10.27  20:50:03 |     3      |
|  6   |  沙僧  |    1    |     二师兄，你也真是的，又要大师兄出马     | 2020.10.27  20:50:59 |     4      |
|  7   | 孙悟空 |    1    |                  我TM...                   | 2020.10.27  20:52:11 |     6      |
|  8   |  沙僧  |    1    |              二师兄，你可以的              | 2020.10.27  20:59:55 |     7      |