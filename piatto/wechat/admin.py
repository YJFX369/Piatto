#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib import admin
from wechat.models import WechatMenuModel
# Register your models here.

# 要使用Django提供的后台管理来添加信息，
# 就要先注册‘模型类’和‘模型管理类’


# 利用装饰器注册模型类和模型管理类
@admin.register(WechatMenuModel)
class WechatMenuModelAdmin(admin.ModelAdmin):
    """定义模型管理类"""
    # 在后台管理系统的界面显示一级菜单名、二级菜单名、菜单类型、回复类型
    list_display = ('button', 'sub_button', 'type', 'key', 'url')



