from django import forms
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.serializers import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# Create your views here.
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from requests import Response


from learn import models
from learn.models import  user
import json as j

class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


# 处理登录的方法
@csrf_exempt
def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        data = UserForm(request.POST)

        if data.is_valid():
            # 获取到表单提交的值
            username = data.cleaned_data['username']
            password = data.cleaned_data['password']
            # 把表单中取到的值和数据库里做对比
            '''存入数据
            new_user = models.user.objects.create()
            new_user.u_name = username
            new_user.u_password = password
            new_user.save()
            '''
            try:
                use = user.objects.get(u_name=username)

                if password == use.u_password:
                    session_list = []  # session列表get_effective_session(session_list) #使用get_effective_session（）方法获取有效session
                    for se in session_list:  # 判断sessionlist中是否有存有该用户登录信息的session,我是把username和user_id(用户标识码存到session中了)
                        if use.user_id == se['user_id']:  # 用户已登录
                            Session.objects.filter(
                                session_key=se.session['session_key'])  # 根据session_key来删除对应session（session开头注意那已经说明）
                            break
                    request.session['username'] = username  # 将用户信息存入新的session中
                    request.session['password'] = password
                    response = HttpResponseRedirect('/index/')
                    return response
                else:
                    response = HttpResponseRedirect('/login/')
                    return response
            except:
                response = HttpResponseRedirect('/login/')
                return response
        else:
            response = HttpResponseRedirect('/login/')
            return response

def index(request):
    return render(request, 'index.html')

def index1(request):

    return render(request, 'index1.html')

def Interface_Table(request,pindex):
    inter_list = models.idetail.objects.all().filter(is_delete=0).order_by("-id")
    p = Paginator(inter_list, 10)  # 实例化Paginator, 每页显示5条数据
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:  # 如果有返回在值，把返回值转为整数型
        int(pindex)
    page = p.page(pindex)  # 传递当前页的实例对象到前端
    return render(request, 'detail.html', {"inter_list": page.object_list, "page": page})

@csrf_exempt
def edit(request,id=-1):
    if request.method == 'GET' and id==-1:
        return render(request, 'edit.html')

    if request.method == 'POST' or id!=-1:
        api_detail = models.idetail.objects.get(id=id)
        detail=api_detail.__dict__
        dict={
            'id': detail['id'],
            'project_name': detail['project_name'],
            'inter_name': detail['inter_name'],
            'inter_describe': detail['inter_describe'],
            'inter_url': detail['inter_url'],
            'inter_menth': detail['inter_menth'],
            'inter_data': detail['inter_data'],
            'status': detail['status'],
            'creater': detail['creater'],
        }
        return render(request, 'edit.html',{"data": dict})

@csrf_exempt
def record_add(request):
    """
    添加解析记录
    :param req:
    :return:
    """
    if request.method == 'POST':
        data = request.body
        data = j.loads(data)
        models.idetail.objects.create(
            project_name=data['project_name'],
            inter_name=data['api_name'],
            inter_describe=data['api_message'],
            inter_url=data['api_url'],
            inter_menth=data['menth'],
            inter_data=data['api_re_message'],
            status=0,
            creater=request.session['username']
        )
        return JsonResponse({"code": 0, "message": "加入成功"})

    else:
        return JsonResponse({"code": -1, "message": "加入失败"})

@csrf_exempt
def delete(request):
    api_id = request.POST['api_id']
    try:
        models.idetail.objects.filter(id=api_id).update(is_delete='1')
        return JsonResponse({"code": 0, "message": "删除成功"})

    except:
        return JsonResponse({"code": -1, "message": "删除失败"})

@csrf_exempt
def stopOrOpen(request):
    api_id = request.POST['api_id']
    status_id= request.POST['status_id']
    try:
        if status_id=='0':
            models.idetail.objects.filter(id=api_id).update(status='1')
        else:
            models.idetail.objects.filter(id=api_id).update(status='0')
        return JsonResponse({"code": 0, "message": "停用/启用成功"})
    except:
        return JsonResponse({"code": -1, "message": "停用/启用失败"})

def postdemo(request):
    if request.method == 'POST':
        dic_params = process_parameters(request.body.decode('utf-8'))   # 一定要用utf-8解码,不然传入的是bytes类型b'body'
        if validate_parameters(dic_params):
            result = read_response()
            res = HttpResponse(result)
            # res.__setitem__("resultcode", '0')  # 用这个也OK, __setitem__可以修改默认的header, 比如Content-Type, setdefault不行
            res.setdefault('resultcode', '0')
            res.setdefault('msg', 'no error')
            return res
        else:
            return HttpResponse('error username or password!')
    else:
        return HttpResponse('error method!')

def mock(request):
    if request.method=='GET':
        print()
    if request.method=='POST':
        print()