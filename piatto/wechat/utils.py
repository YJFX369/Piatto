#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# utils.py用于存放工具函数

from wechat.models import WechatMenuModel
from wechatpy import WeChatClient
from django.http import HttpResponse, JsonResponse


def del_dict_null(dic):
    """删除字典dic中的空值"""
    dic_copy = dic.copy()
    for i in dic_copy.keys():
        if not dic_copy[i]:
            del dic[i]


def _get_main_button_index(buttons, name):
    """当遇见重复的一级菜单时，获取该菜单在buttons中的指针，以确定在buttons的哪个位置插入字典"""
    for index, button in enumerate(buttons):
        if button['name'] == name:
            return index


def _get_button_dict(button_obj, is_sub=False):
    """将button中的数据组成微信API规定格式的字典"""
    button_dict = dict(type=button_obj.type, key=button_obj.key, url=button_obj.url)
    if is_sub:
        button_dict['name'] = button_obj.sub_button
    else:
        button_dict['name'] = button_obj.button
    del_dict_null(button_dict)  # 删除字典中的空值
    return button_dict


def create_menu():
    """
    1. 筛选在django管理平台上添加的菜单具体数据，转化为符合微信API要求的格式，
    2. 创建微信菜单
    """
    buttons = []  # 最终需要的列表
    menues_name = set()  # 由一级菜单构成的集合
    menues = WechatMenuModel.objects.all()  # menus即mysql数据库中的rows，就是在models.py中定义的field
    # 遍历一级菜单
    for menu in menues:
        if not menu.sub_button:  # 如果这个menu中没有二级菜单
            buttons.append(_get_button_dict(menu, False))  # 将is_sub=False时（即一级菜单）组成的字典添加到buttons中。
            menues_name.add(menu.button)  # 将一级菜单添加到set
            continue
        if menu.button in menues_name:  # 当遇见重复的一级菜单名
            index = _get_main_button_index(buttons, menu.button)  # 获取指针
            # 将is_sub=True时（即二级菜单）组成的字典添加到 buttons中的列表'sub_button'内。
            buttons[index]['sub_button'].append(_get_button_dict(menu, True))
        else:  # 如果这个menu中有二级菜单
            menues_name.add(menu.button)
            buttons.append(dict(name=menu.button, sub_button=[_get_button_dict(menu, True)]))

    # app_id = 'wx016600bf7d732ec0'
    # app_secret = '38efecf06803374248e620977691f987'
    # # WeChatClient()第一个参数是公众号里面的appID，第二个参数是appsecret
    # client = WeChatClient(app_id, app_secret)
    # # 创建自定义菜单
    # new_menu = client.menu.create({'button': buttons})
    # return JsonResponse(new_menu, safe=False)
    return JsonResponse({'button': buttons}, safe=False)

















