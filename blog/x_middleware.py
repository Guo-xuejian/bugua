import time

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
from blog import models


# 中间件 白名单 不需要登录就能访问的页面
class WhiteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        whitelist = {"/", "/admin/", "/index/", "/login/", "/register/", "/check_username/", "/get_rgb/",
                     "/get_valid_code/", "/article_detail/", "/article_detail/"}
        target_url = request.path

        for url in whitelist:
            if target_url in url:
                return

        if not request.user.username:
            return redirect(f'/login/?next={target_url}')


# 访问平台记录日志
class PlatformMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        url = request.get_full_path()
        device = request.META['HTTP_USER_AGENT']
        platform = request.META['HTTP_USER_AGENT']
        if ('Mozilla' in device) and ('AppleWebKit' in device) and ('Chrome' in device) and ('Safari' in device) and (
                'SE' in device):
            device = '搜狗浏览器'
        elif ('Mozilla' in device) and ('AppleWebKit' in device) and ('Chrome' in device) and ('Safari' in device) and (
                'Edge' in device):
            device = 'Edge浏览器'
        elif ('Mozilla' in device) and ('AppleWebKit' in device) and ('Chrome' in device):
            device = '谷歌浏览器'
        elif 'Safari' in device:
            device = 'Safari浏览器'
        elif 'Firefox' in device:
            device = '火狐浏览器'
        elif 'QQ' in device:
            device = 'QQ浏览器'
        elif 'Opera' in device:
            device = 'Opera浏览器'
        elif '360' in device:
            device = '360浏览器'
        elif 'MicroMessenger' in device:
            device = '微信浏览器'
        elif 'UC' in device:
            device = 'UC浏览器'
        elif 'Quark' in device:
            device = '夸克浏览器'
        elif '2345' in device:
            device = '2345浏览器'
        elif 'XiaoMi' in device:
            device = '小米浏览器'
        elif 'SamsungBrowser' in device:
            device = '三星浏览器'
        else:
            device = 'IE浏览器'

        if 'Windows NT 5.1' in platform:
            platform = 'Windows XP'
        elif 'Windows NT 5.2' in platform:
            platform = 'Windows 2003'
        elif 'Windows NT 6.0' in platform:
            platform = 'Windows Vista'
        elif 'Windows NT 6.1' in platform:
            platform = 'Windows 7'
        elif 'Windows NT 10' in platform:
            platform = 'Windows 10'
        elif 'Windows' in platform:
            platform = 'Windows'
        elif 'Mac OS X' in platform:
            platform = 'Mac OS X'
        elif 'Linux' in platform:
            platform = 'Linux'
        else:
            platform = '未知平台'
        log_obj = models.Log(ip=ip, url=url, device=device, platform=platform)
        log_obj.save()


# 频率限制
class FrequentMiddleware(MiddlewareMixin):
    visit_ip_pool = {}

    def process_request(self, request):
        ip = request.META.get("REMOTE_ADDR")
        visit_time = time.time()
        if ip not in FrequentMiddleware.visit_ip_pool:
            FrequentMiddleware.visit_ip_pool[ip] = [visit_time]
        history_time = FrequentMiddleware.visit_ip_pool.get(ip)
        while history_time and visit_time - history_time[-1] > 60:
            history_time.pop()
        if len(history_time) < 10:
            history_time.insert(0, visit_time)
        else:
            return HttpResponse("访问过于频繁,还需等待%s秒才能继续访问" % int(60 - (visit_time - history_time[-1])))
