import datetime

from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from Login.models import User, RegisterForm


# Create your views here.
# 装饰器，路由保护
# def check_login(func):
#     def inner(*args,**kwargs):
#         print(args,kwargs)
#         #if args[0].COOKIES.get('username'):
#         if args[0].session.get('username'):
#             return func(*args,**kwargs)
#         else:
#             return redirect(reverse('Login:login'))
#         # return func(*args,**kwargs)
#     return inner

# def login(request):
#     if request.method == "POST":
#         userinfo = request.POST.dict()
#         userinfo.pop("csrfmiddlewaretoken")
#         print(userinfo)
#         # user = User.objects.filter(**userinfo).first()
#         user = User.objects.filter(username=userinfo.get('username'), password=userinfo.get('password')).first()
#         if user:
#             # response = redirect('Login/login_two_columns.html')
#             # cookie
#             # # 三天以后过期
#             # future = datetime.now() + timedelta(days=3)
#             # # 将cookie协会客户端
#             # response.set_cookie('username',user.username,expires=future)
#
#             # session
#             print(user.username)
#             request.session['username'] = user.username
#             request.session['uid'] = user.uid
#             request.session.set_expiry(timedelta(days=1))
#             return render(request, "base.html", context=locals())
#     return render(request, "Login/login_two_columns.html")
#
# def logout(request):
#     # res = redirect('Login/login_two_columns.html')
#     # 删除cookie
#     # res.delete_cookie("username")
#
#     # 清楚session
#     # request.session.clear() # 清除所有session键值对,不清空sessionid
#     request.session.flush() # 清除所有session键值对,清空sessionid,并清空数据库对应的记录
#     #del request.session['username'] # 清除指定session键值对
#     return redirect(reverse('Login:login'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 用户验证，如果用户名和密码正确，返回User的对下，否则返回None
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            # 记录用户登录状态，参数是请求对象和用户对象
            login(request, user)

            return redirect(reverse("App:index"))
        else:
            return render(request, 'Login/login_two_columns.html', {'msg': '用户名和密码错误'})
    return render(request, "Login/login_two_columns.html")

def user_logout(request):
    # 退出登录
    logout(request)
    return redirect(reverse("Login:login"))

def user_register(request):
    if request.method == "POST":
        # 用提交的数据生成表单
        form = RegisterForm(request.POST)
        # 能通过验证，返回True，否则返回False
        if form.is_valid():
            # 进行业务处理
            data = form.cleaned_data
            data.pop("confirm")
            # 获取指定字段
            username = form.cleaned_data.get('username','')
            password = form.cleaned_data.get('password', '')
            print(username + "|" + password)
            # print(data,type(data))
            # 如果forms中表单的字段名和models模型的字段名一致
            # 把用户写入数据库
            # 密码会做签名，不能手动签名加密password
            data['regtime'] = str(datetime.date.today())
            data['jurisdiction'] = 1
            res = User.objects.create_user(**data)
            # 如果forms中表单的字段名和models模型的字段名不一致
            # res = User.objects.create(username=username,password=form.cleaned_data.get('password'))
            if res:
                return redirect(reverse("Login:login"))#render(request, "Login/login_two_colmns.html")
            else:
                print("注册错误", res)
        else:
            print(form.__dict__)
            # 验证不成功，把错误信息渲染到前端页面
            return render(request, "Login/register.html", {'form': form})
    else:
        form = 0
        return render(request, "Login/register.html",{'form': form})

def change_password(request):
    # 修改密码
    user = User.objects.get(pk=1)
    user.set_password('123')
    user.save()
    return HttpResponse("修改密码")
