#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""piatto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 配置全局 url， 指向 wechat 应用的 url
    # include() 的作用就是将app的url在project的urls.py中进行注册。

    #  include((urlconf_module, app_name), namespace=None)
    #  第一个元素urlconf_module是app的url文件的位置，
    #  第二个元素是app的名字，
    #  第三个元素是命名空间。
    #  可以不传入app_name, 也可以不传入namespace, 甚至两个都不传入也都OK.
    #  但是...不可以只传入namespace!
    path('wechat/', include(('wechat.urls', 'wechat'), namespace='wechat')),
]
