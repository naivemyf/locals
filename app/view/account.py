import json

from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect
from app import models
from app.utils.code import check_code
from app.utils.form import RegisterForm, LoginForm, Adminreset
from app.utils.bootsrap import BootsrapForm,BootsrapModel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.utils.pagination import Pagination


#注册
def register(req):
    """注册"""
    if req.method == "GET":
        form = RegisterForm()
        return render(req, 'user/register.html', {'form': form})
    form = RegisterForm(data=req.POST)
    if form.is_valid():
        req.session["account"] = form.cleaned_data.get("username")
        form.instance.role_id = 1
        form.save()
        return redirect("/chocies/fav/")
    return render(req, 'user/register.html', {'form': form})

 # elif rid == 2:
        #     form.instance.process = 0
        #     form.save()
        #     return HttpResponse('<p style="text-align:center;font-size: 60px">注册成功，请等待管理员审核<p>')
        # elif rid == 3:
        #     return HttpResponse('<p style="text-align:center;font-size: 60px">管理员无需注册<p>')


# 登录
def login(req):
    """登录"""
    if req.method == "GET":
        form = LoginForm()
        return render(req, 'user/login.html', {'form': form})

    form = LoginForm(data=req.POST)
    if form.is_valid():
        # 验证成功,获取用户名和密码
        #print(form.cleaned_data) 打印加密后的值
        # 获取的值
        # {'username': 'xxxx', 'password':‘xxxxxxxxxxxxxxxx'}
        # form.cleaned_data["code"]
        # 将输入的验证码从框架获取数据的字典中删除

        # 验证码校验
        user_input_code = form.cleaned_data.pop("code")
        code = req.session.get("image_code", "")
        if code.upper() != user_input_code:
            form.add_error("code", "验证码错误")
            return render(req, "user/login.html", {"form": form})

        # 数据库检验用户名和密码
        # models.Admin.objects.filter(username='form.cleaned_data['username']',password='form.cleaned_data['password']').first()
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或者密码错误！")  # 显示错误信息在password框下面
            return render(req, 'user/login.html', {'form': form})

        # 网站生成随机字符串，写到用户浏览器的cookie和session中
        req.session["info"] = {
            'id': admin_object.id,
            'name': admin_object.username,
            "role_id": admin_object.role_id}
        # 七天免登录
        req.session.set_expiry(60 * 60 * 24 * 7)

        rid = admin_object.role_id
        if rid == 1:#普通使用者
            return redirect('/index/')#信息正确，跳转首页
        elif rid == 2 and admin_object.process == 0:#未审核商家
            return HttpResponse('<p style="text-align:center;font-size: 60px">注册成功，请等待管理员审核<p>')
        elif rid == 2 and admin_object.process == 1:#已审核商家
            return redirect("/merchant/")
    return render(req, 'user/login.html', {'form': form})

# 生成验证码
def image_code(req):
    """生成验证码"""
    img, code = check_code()
    # 写入session，以便验证
    req.session["image_code"] = code
    # session设置60秒超时
    req.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())#返回图片

# 注销
def logout(req):
    """注销"""
    req.session.clear()
    return redirect("/index/")


# 收藏列表
def favindex(req):
    title = "我的文章收藏"


    uname = req.session["info"]["name"]  # 获取用户名
    # art_ids = models.Enshrine.objects.filter(username=uname, art_id__isnull=False).values_list('art_id',flat=True)
    # # 搜素用户名和文章id不为空的数据，并取出满足两个条件的文章id用列表（一维表）的形式储存
    existsts = models.Enshrine.objects.filter(username=uname, art_id__isnull=False).exists()
    if not existsts:
        return render(req,'user/list_favorite.html', {'title': title})
    u_list =models.Enshrine.objects.filter(username=uname,status=1)  # 查找用户储存的收藏信息
    article_list = []   # 列表
    for i in u_list:
        art_id = i.art_id  # 将数据信息的id取出
        exists =models.Article.objects.filter(id=art_id).exists()  # 用id到文章表查找是否存在
        if not exists:  # 文章不存在，跳出此次循环
            continue
        art = models.Article.objects.get(id=art_id)  # 文章存在，则将文章信息取出
        if not art:  # 文章不存在，跳出此次循环
            continue
        time =i.enshrinetime  # 取出收藏时间
        article_list.append({
            'art': art,
            'time': time,
        })
    if not article_list:
        message = "抱歉，您收藏的文章被删除了！"
        return render(req, 'user/list_favorite.html', {'title': title, 'message': message})
    return render(req,'user/list_favorite.html', {'title': title, 'art': article_list})


#  我的商品收藏
def favindexcomm(req):
    title = "我的商品收藏"

    uname = req.session["info"]["name"]  # 获取用户名
    # art_ids = models.Enshrine.objects.filter(username=uname, art_id__isnull=False).values_list('art_id',flat=True)
    # # 搜素用户名和文章id不为空的数据，并取出满足两个条件的文章id用列表（一维表）的形式储存
    exists =models.Enshrine.objects.filter(username=uname, comm_id__isnull=False).exists()
    if not exists:
        return render(req, 'user/list_favorite.html', {'title': title})
    u_list = models.Enshrine.objects.filter(username=uname,status=1)
    comm_list = []
    for i in u_list:
        comm_id = i.comm_id
        if not comm_id:
            continue
        existsid = models.Commdity.objects.filter(id=comm_id).exists()  # 查询收藏的商品是否存在
        if not existsid:
            continue
        comm = models.Commdity.objects.get(id=comm_id)
        time = i.enshrinetime
        comm_list.append({
            'comm': comm,
            'time': time,
        })
        if not comm_list:
            message = "抱歉，您收藏的商品被删除了！"
            return render(req, 'user/list_favorite.html', {'title': title, 'message': message})
    return render(req, 'user/list_favorite.html', {'title': title, 'comm': comm_list})

class Myinfo(BootsrapModel):
    class Meta:
        model = models.User
        fields=["username","phonenumber"]
#  我的信息
def myinfo(req,nid):
    if req.method == "GET":
        obj = models.User.objects.filter(id=nid).first()
        name = req.session["info"]["name"]
        form = Myinfo(instance=obj)
        pd = Adminreset()
        art = models.Article.objects.filter(username=name,status=1).all()
        art_list = []
        for i in art:
            if i.message:
                art_dict ={
                    "id":i.id,
                    "mes":i.message,
                    "time":i.timemes,
                    "title":i.title,
                    "createtime":i.timestamp,
                }
                art_list.append(art_dict)
        return render(req, 'user/user_mess.html', {'obj': obj,"art":art_list,"form":form,"pd":pd})
    # return render(req,'user/user_mess.html',{'form':form})


@csrf_exempt
def edit_myinfo(req):
    if req.method == "POST":
        uid = req.GET.get("uid")
        obj = models.User.objects.filter(id=uid).first()
        if not obj:
            return JsonResponse({
                "status": False,
                "tips": "修改失败，数据不存在",
            })
            # JsonResponse返回状态Flase和错误
        forms = Myinfo(data=req.POST, instance=obj)

        if forms.is_valid():
            forms.save()
            data_dict = {"status": True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {"status": False, 'error': forms.errors}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))  # 返回状态Flase和错误



@csrf_exempt
def edit_pd(req):

    if req.method == "POST":
        uid = req.GET.get("uid")
        obj = models.User.objects.filter(id=uid).first()
        if not obj:
            return JsonResponse({
                "status": False,
                "tips": "修改失败，数据不存在",
            })
            # JsonResponse返回状态Flase和错误
        forms = Adminreset(data=req.POST, instance=obj)
        if forms.is_valid():
            forms.save()
            data_dict = {"status": True}
            return HttpResponse(json.dumps(data_dict))
        data_dict = {"status": False, 'error': forms.errors}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
#
def mess_list(req):
    title = "公告列表"
    list = models.Message.objects.all()
    page_obj = Pagination(req, list)
    context = {
        "title": title,
        "list": page_obj.page_queryset,
        "page_string": page_obj.html(),
    }
    return render(req,"user/mess_list.html",context)