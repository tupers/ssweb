# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse
from .ssservice import ssService
from models import User,Order
import json

# Create your views here.

def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、确认密码、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    # 将记录用户注册前页面的 redirect_to 传给模板，以维持 next 参数在整个注册流程中的传递
    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})

def index(request):
    response = HttpResponse()
    user = request.user
    datausage=-1
    #if user.is_authenticated() and (not user.service==-1):
    if user.is_authenticated():
        # remote = ssService('127.0.0.1',7000,0.5)
        # info = remote.cmd("get{%d}"%int(user.service))
        # remote.close()
        # info = str(info)
        # info = info[info.find('(')+1:info.find(')')]
        # userinfo = info.split(",")
        #datausage = float(userinfo[1])+float(userinfo[2])
        datausage = 0.0
    return render(request, 'index.html', context={'datausage':datausage})

def request_check(request):
    #response = HttpResponse()
    user = request.user
    if request.is_ajax() and user.is_authenticated():
        return True
    else:
        return False

def addservice(request):
    if request_check(request):
        pwd =  request.POST["password"]
        port = request.POST["port"]
        remote = ssService('127.0.0.1',7000,0.5)
        ret = remote.cmd("add{%s,%s}"%(port,pwd))
        if ret=="ok":
            user = User.objects.get(username=request.user)
            user.service = port
            user.save()
        ret = {"status":"%s"%ret}
        return HttpResponse(json.dumps(ret))
    else:
        return redirect('/')
    '''
    response = HttpResponse()
    user = request.user
    if user.is_authenticated():
        remote = ssService('127.0.0.1',7000,0.5)
        ret = remote.cmd("port_available")
        remote.close()
        return HttpResponse("Available port number:%s"%ret)
    else:
        return HttpResponse("Need Login Fisrt")
    '''

def service_list(request):
    if request.method == 'POST':
        if request_check(request):
            password = request.POST["password"]
            plan_dict = eval(request.POST["plan"])
            ret = {"result": "success", "port": 7890, "ip": "35.200.82.164"}
            return HttpResponse(json.dumps(ret))
        else:
            return redirect('/')
    else:
        group = request.GET.get('group', '')
        plan = request.GET.get('plan', '')
        if group == '' or plan == '':
            group = 0
            plan = 0
        return render(request, 'users/service_list.html', context={'group': group, 'plan': plan})

def get_orders(name):
    user_id = User.objects.get(username=name).id
    try:
        orders = Order.objects.filter(owner=user_id, status__gt=0)
        return orders
    except Order.DoesNotExist:
        return []

def user_center(request):
    user = request.user
    if user.is_authenticated():
        # search form order according username
        orders = get_orders(user)
        return render(request, 'users/user_center.html', context={'orders': orders})
    else:
        return render(request, 'users/user_center.html')

def get_order_info(request):
    if request.method == 'POST':
        if request_check(request):
            order_id = request.POST["id"]
            order = Order.objects.get(id=order_id)
            # get information from ssdb by udp
            if int(order_id) == 1:
                ret = "{\"result\":\"success\",\"port\":%d,\"ip\":[\"35.200.82.164\",\"35.200.14.2\"],\"dataUsage\":50,\"dataLimit\":150}"%order.port
            else:
                ret = "{\"result\":\"success\",\"port\":%d,\"ip\":[\"35.200.82.164\",\"35.200.14.2\"],\"dataUsage\":30,\"dataLimit\":300}" % order.port

            return HttpResponse(ret)
        else:
            return redirect('/')
    else:
        return redirect('/')
