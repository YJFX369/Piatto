#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path
from wechat import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('news/', views.news, name='news'),
]
