#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.
# 定义数据模型


class WechatMenuModel(models.Model):
    """微信自定义菜单模型类"""

    Menu_type = (
        ('click', '事件推送'),
        ('view', '跳转网页')
    )

    button = models.CharField(max_length=16, verbose_name='一级菜单',
                              help_text='一级菜单可设置1~3个，每个菜单最多4个汉字')
    # null=True, blank=True 表示在数据库及django后台管理中都允许为空
    sub_button = models.CharField(max_length=28, verbose_name='二级菜单', null=True, blank=True,
                                  help_text='二级菜单可设置1~5个，每个菜单最多7个汉字')
    type = models.CharField(max_length=100, verbose_name='菜单类型', choices=Menu_type)

    key = models.CharField(max_length=128, verbose_name='event', null=True, blank=True,
                           help_text='菜单的key值，')

    url = models.URLField(max_length=1024, verbose_name='url', null=True, blank=True,
                          help_text='菜单类型为view时必填')

    def __str__(self):
        return self.button

    # 可以通过在模型类中定义Meta类来修改表名：
    class Meta:
        db_table = 'tb_wechat_menu'
        # 默认数据库表在后台中显示都为复数形式，
        # 而中文没有复数形式，因此将两种形式都设置为相同名称修改结果。
        verbose_name = '菜单'
        verbose_name_plural = '菜单'
