# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import HttpResponse,JsonResponse
from .ssservice import ssService
from models import User,Order,Plan
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
    user = request.user
    orders = []
    if user.is_authenticated():
        orders = get_orders(user)
    return render(request, 'index.html', context={'orders':orders})

def request_check(request):
    #response = HttpResponse()
    user = request.user
    if request.is_ajax() and user.is_authenticated():
        return True
    else:
        return False

def service_list(request):
    if request.method == 'POST':
        if request_check(request):
            orders = get_orders(request.user)
            user_id = User.objects.get(username=request.user).id
            #normal user only can creat one order
            if len(orders)>0 and user_id != 1:
                ret = "{\"ret\":\"failed\"}"
                return HttpResponse(ret)

            password = request.POST["password"]
            plan = Plan.objects.get(id = int(request.POST["plan"]))
            
            #cmd add and insert in order list
            #ignore plan for temporary
            remote = ssService('127.0.0.1',9003,0.5)
            ret = remote.cmd("{\"cmd\":\"add\",\"password\":\"%s\",\"dataLimit\":%d,\"peroid\":%d,\"peroid_times\":%d}"%(password,plan.data_limit,plan.peroid,plan.peroid_times));
            remote.close()
            ret_json = json.loads(ret)
            if ret_json["ret"] == "success":
                #add order
                order = Order(port=int(ret_json["port"]),ip_group=int(ret_json["ip_group"]),strategy=plan.id,owner=user_id,status=1)
                order.save()
                
            return HttpResponse(ret)
        else:
            return redirect('/')
    else:
        plans = []
        plans = Plan.objects.all()
        group = request.GET.get('group', '')
        plan = request.GET.get('plan', '')
        if group == '' or plan == '':
            group = 0
            plan = 0
        return render(request, 'users/service_list.html', context={'group': group, 'plan': plan, 'plans':plans})

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
            remote = ssService('127.0.0.1',9003,0.5)
            ret = remote.cmd("{\"cmd\":\"get\",\"port\":%d,\"group\":%d}"%(order.port,order.ip_group));
            remote.close()
            return HttpResponse(ret)
        else:
            return redirect('/')
    else:
        return redirect('/')

def get_auth_obj(request):
    import hmac,hashlib,time
    gateone_server = 'http://127.0.0.1:8000'
    api_key = "ZGE4Yzg4YWM4YzkwNDU4YTgzNWRmYzBhM2UyNTQ0ZmFmM"
    secret = "NzlkNjNjZGI2ZWIyNGE1NDgzNTg4YzAxYjY0YmFmNDBkY"
    authobj = {
            'api_key':api_key,
            'upn':'gateone',
            'timestamp':str(int(time.time()*1000)),
            'signature_method':'HMAC-SHA1',
            'api_version':'1.0'
            }

    hash = hmac.new(str(secret),digestmod=hashlib.sha1)
    hash.update(authobj['api_key']+authobj['upn']+authobj['timestamp'])
    authobj['signature'] = hash.hexdigest()
    auth_info_and_server = {'url':gateone_server,'auth':authobj}
    return JsonResponse(auth_info_and_server)

