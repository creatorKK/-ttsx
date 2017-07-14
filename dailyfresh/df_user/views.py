#coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from models import *
from hashlib import sha1
import datetime
from login_check import *

# Create your views here.

def index(request):
    return render(request, 'index')

def register(request):
    context = {'title':'注册','top':'0'}
    return render(request, 'df_user/register.html', context)

def register_handle(request):
    #接收数据
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    umail = post.get('user_email')
    #加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    #创建对象
    user = UserInfo()
    user.uname=uname
    user.upwd = upwd_sha1
    user.umail = umail
    user.save()
    #完成后转向
    return redirect('/user/login/')
def register_valid(request):
    uname=request.GET.get('uname')
    result=UserInfo.objects.filter(uname=uname).count()
    context={'valid':result}
    return JsonResponse(context)

def login(request):
    context={'title':'登录','top':'0'}
    return render(request, 'df_user/login.html',context)

def login_handle(request):
    global login_ok
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    uname_jz = post.get('name_jz', '0')

    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    context = {'title':'登录', 'uname':uname, 'upwd':upwd, 'top':'0'}
    users = UserInfo.objects.filter(uname=uname)
    if len(users)==0:
        context['name_error']='1'
        return render(request, 'df_user/login.html', context)
    else:
        if users[0].upwd==upwd_sha1:
            request.session['uid']=users[0].id
            request.session['uname']=uname
            #跳转回原页面
            path = request.session.get('url_path', '/')
            response=redirect(path)

            if uname_jz=='1':
                response.set_cookie('uname', uname, expires=datetime.datetime.now()+datetime.timedelta(days = 7))
            else:
                response.set_cookie('uname','',max_age=-1)

            return response

        else:
            context['pwd_error']='1'
            return render(request, 'df_user/login.html',context)
def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def islogin(request):
    result=0
    if request.session.has_key('uid'):
        result=1
    return JsonResponse({'islogin':result})

@denglu_yanzheng
def center(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    context = {'title':'用户中心','user':user}
    return render(request, 'df_user/center.html', context)

@denglu_yanzheng
def order(request):
    context = {'title':'用户订单'}
    return render(request,'df_user/order.html',context)

@denglu_yanzheng
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method=='POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.ucode = post.get('ucode')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'收货地址', 'user':user}
    return render(request, 'df_user/site.html', context)




# def query(request):
#     return render(request,'df_user/query.html')


