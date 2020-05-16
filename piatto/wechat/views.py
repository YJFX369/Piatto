#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from wechatpy import parse_message  # 解析xml
from wechatpy import create_reply  # 快速回复消息
from wechatpy.replies import TextReply  # 回复text消息
from wechatpy.utils import check_signature  # 检查signature
from wechatpy.exceptions import InvalidSignatureException  # 捕获错误

from .utils import create_menu


def menu(request):
    """
    导入create_menu()
    """
    return create_menu()


def news(request):
    """
    所有的消息都会先进入这个函数进行处理，包含两个功能：
        1.微信接入验证是用GET请求；
        2.微信收发消息是用POST请求，传输消息类型是xml。
    """

    TOKEN = 'piatto'  # 服务器配置中的token
    if request.method == 'GET':
        """
        微信服务器发送GET请求到指定的服务器URL上，
        GET请求携带参数包括signature、timestamp、nonce、echostr，
        服务端程序通过检验signature对请求进行校验。
        若确认此次GET请求来自微信服务器，则原样返回echostr参数内容给微信服务器，微信服务器确认后此次接入才会生效。
        """
        # 接受微信服务器get请求中的参数
        # request.GET('x') 如果GET请求中没有参数 x ，会报错。
        # request.GET.get('x', None) 如果GET请求中没有参数 x ，会返回 None ，不会报错。
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echo_str = request.GET.get('echostr', None)

        # # 服务器配置中的token
        # token = TOKEN
        #
        # # 把参数放到list中排序后合成一个字符串，
        # # 再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过。
        # hash_list = [token, timestamp, nonce]
        # hash_list.sort()
        # hash_str = ''.join([x for x in hash_list])
        # # 使用sha1加密
        # hash_str = hashlib.sha1(hash_str.encode('utf-8')).hexdigest()
        # if signature == hash_str:
        #     return HttpResponse(echo_str)
        # else:
        #     return HttpResponse('signature error')

        try:
            # check_signature()检查signature是否正确， 若正确则自动返回echostr， 若错误则捕获错误。
            check_signature(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'signature error'
        return HttpResponse(echo_str)

    else:  # 即 request.method == 'POST'
        """
        微信消息类型是xml，
    例：
        用户给公众号发送文本消息：我是津巴布韦小将，
        在开发者后台，收到公众平台发送的xml 如下：
        <xml>
        <ToUserName><![CDATA[公众号]]></ToUserName>
        <FromUserName><![CDATA[用户号]]></FromUserName>
        <CreateTime>1460537339</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[我是津巴布韦小将]]></Content>
        <MsgId>6272960105994287618</MsgId>
        </xml>

        CreateTime 是微信公众平台记录用户发送该消息的具体时间
        MsgType: 用于标记该xml 是什么类型消息【这里是text类型】，一般用于区别判断
        Content: 说明该用户发给公众号的具体内容是【我是津巴布韦小将】
        MsgId: 是公众平台为记录识别该消息的一个标记数值, 微信后台系统自动产生
        """

        # 使用 wechatpy 中的 parse_message 作为解析器，解析微信服务器发送的 XML 消息
        weixin_msg = parse_message(request.body)
        if weixin_msg.type == 'text':
            # 利用 wechatpy 的 create_reply 进行快速回复
            resp = create_reply('文字已收到！', weixin_msg)
        elif weixin_msg.type == 'image':
            resp = create_reply('图片已收到！', weixin_msg)
        elif weixin_msg.type == 'voice':
            resp = create_reply('语音已收到！', weixin_msg)
        else:
            resp = create_reply('无法识别此类型的消息！', weixin_msg)
        # render() 将python类中的reply渲染为xml
        post_response = resp.render()
        return HttpResponse(post_response)































