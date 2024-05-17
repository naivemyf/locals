# from app.utils.pagination import Pagination
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from app import models
from django import forms
from app.utils.bootsrap import BootsrapModel
# from app.utils.form import Adminreset, AdminUpadte, AdminModelForm
from datetime import datetime

from app.utils.form import LoginForm
from app.utils.pagination import Pagination

def login(req):
    """登录"""
    if req.method == "GET":
        form = LoginForm()
        return render(req, 'admin/ad_login.html', {'form': form})

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
            return render(req, "admin/ad_login.html", {"form": form})

        # 数据库检验用户名和密码
        # models.Admin.objects.filter(username='form.cleaned_data['username']',password='form.cleaned_data['password']').first()
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或者密码错误！")  # 显示错误信息在password框下面
            return render(req, 'admin/ad_login.html', {'form': form})

        # 网站生成随机字符串，写到用户浏览器的cookie和session中
        req.session["info"] = {
            'id': admin_object.id,
            'name': admin_object.username,
            "role_id": admin_object.role_id}
        # 七天免登录
        req.session.set_expiry(60 * 60 * 24 * 7)

        rid = admin_object.role_id
        if rid == 3:#管理员
            return redirect("/admin/")
    return render(req, 'admin/ad_login.html', {'form': form})

# 所有审核数量
def adminindex(req):
    art_counts = models.Article.objects.filter(status=1).count()
    comm_counts = models.Commdity.objects.filter(status=0).count()
    me_counts = models.User.objects.filter(process=0).count()
    data={
        "art_counts": art_counts,
        "comm_counts": comm_counts,
        "me_counts": me_counts
    }

    return render(req, "admin/admin.html", {"data": data})

# 审核饼图
def chart_pie(req):
    art_counts = models.Article.objects.filter(status=1).count()
    comm_counts = models.Commdity.objects.filter(status=0).count()
    me_counts = models.User.objects.filter(process=0).count()
    data = [
        {"value": art_counts, "name": '文章'},
        {"value": comm_counts, "name": '特色产品'},
        {"value": me_counts, "name": '商家'},
    ]
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)
def analyse_index(req):
    return render(req,"admin/chat.html")

# 文章饼图分析
def art_chartpie(req):
    tags = models.Choice.objects.all().values('id', 'name')
    # 对每个标签，获取其对应的文章数量
    for tag in tags:
        tag['value'] = models.Article.objects.filter(tag=tag['name']).count()
    data = list(tags)
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)

def comm_chartpie(req):
    tags = models.Choice.objects.all().values('id', 'name')
    # 对每个标签，获取其对应的文章数量
    for tag in tags:
        tag['value'] = models.Commdity.objects.filter(tag=tag['name']).count()
    data = list(tags)
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)
class Ad_art(BootsrapModel):
    class Meta:
        form = models.Article
        fields = "__all__"

#  未审核文章列表
def ad_art_list_no(req):
    """未审核文章列表"""
    title='未审核文章'
    art_list = models.Article.objects.filter(status=1).all()
    return render(req,"admin/ad_art_list.html", {'art_list': art_list, "title": title})

#  文章列表
def ad_art_list(req):
    """所有文章列表"""
    title = '所有文章'
    art_list = models.Article.objects.all()
    return render(req,"admin/ad_art_list.html", {'art_list': art_list, "title": title})

#  商家列表
def ad_me_listno(req):
    """未审核商家列表"""
    title = '未审核商家'
    me_list = models.User.objects.filter(process=0).all()
    return render(req, "admin/ad_me_list.html", {'me_list': me_list, "title": title})

#  未审核商家
def ad_me_list(req):
    """未审核商家列表"""
    title = '所有商家'
    me_list = models.User.objects.filter(role=2).all()
    return render(req, "admin/ad_me_list.html", {'me_list': me_list, "title": title})

#  未审核商品
def ad_comm_listno(req):
    title = "未审核商品"
    comm_list = models.Commdity.objects.filter(status=0).all()
    return render(req, "admin/ad_comm_list.html", {"title": title, "comm_list": comm_list})

#  商品列表
def ad_comm_list(req):
    title = "所有商品"
    comm_list = models.Commdity.objects.all()
    return  render(req, "admin/ad_comm_list.html", {"title": title, "comm_list": comm_list})

#  文章信息
def art_detail(req,nid):
    title= "文章信息"
    obj = models.Article.objects.filter(id=nid).first()
    if not obj:
        return redirect("article/listme")
    return render(req, "user/list_content.html", {"obj": obj,"title":title})

# 商品信息
def comm_detail(req,nid):
    title = "商品信息"
    obj= models.Commdity.objects.filter(id=nid).first()
    if not obj:
        messages.error(req,"商品不存在！")
    return render(req,"user/list_content.html",{"obj":obj,"title":title})

#  审核商品操作
def comm_status(req):
    uid = req.GET.get("uid")
    obj = models.Commdity.objects.filter(id=uid).first()
    if not obj:
        return JsonResponse({
            "status": False,
            "error": "审核失败，数据出错",
        })  # JsonResponse返回状态Flase和错误
    models.Commdity.objects.filter(id=uid).update(status=1)
    return JsonResponse({"status": True})

#  批量审核商品
def comm_batch(req):
    if req.method == 'POST':
        uids = req.POST.getlist('uids[]')
        for uid in uids:
            obj = models.Commdity.objects.filter(id=uid).first()
            if not obj:
                return JsonResponse({
                    "status": False,
                    "error": "审核失败，数据出错",
                })
            models.Commdity.objects.filter(id=uid).update(status=1)
        return JsonResponse({'status': True})

# 未审核通过商品意见
def comm_nostatus(req):
    if req.method == 'GET':
        uid = req.GET.get('uid')
        res = req.GET.get('res')
        timemes = datetime.now()
        obj = models.Commdity.objects.filter(id=uid).first()
        if not obj:
            return JsonResponse({
                "status": False,
                "error": "审核失败，数据出错",
            })
        models.Commdity.objects.filter(id=uid).update(message=res,timemes=timemes)
        return JsonResponse({'status': True})

#  审核文章
def art_status(req):
    uid = req.GET.get("uid")
    obj = models.Article.objects.filter(id=uid).first()
    if not obj:
        return JsonResponse({
            "status": False,
            "error": "审核失败，数据出错",
        })  # JsonResponse返回状态Flase和错误
    models.Article.objects.filter(id=uid).update(status=2)
    return JsonResponse({"status": True})

#  批量审核文章
def art_batch(req):
    if req.method == 'POST':
        uids = req.POST.getlist('uids[]')
        for uid in uids:
            obj = models.Article.objects.filter(id=uid).first()
            if not obj:
                return JsonResponse({
                    "status": False,
                    "error": "审核失败，数据出错",
                })
            models.Article.objects.filter(id=uid).update(status=2)
        return JsonResponse({'status': True})

# 未审核通过文章意见
def art_nostatus(req):
    if req.method == 'GET':
        uid = req.GET.get('uid')
        res = req.GET.get('res')
        timemes = datetime.now()
        obj = models.Article.objects.filter(id=uid).first()
        if not obj:
            return JsonResponse({
                "status": False,
                "error": "审核失败，数据出错",
            })
        models.Article.objects.filter(id=uid).update(message=res,timemes=timemes)
        return JsonResponse({'status': True})
#商家详情
def me_detail(req,nid):
    title = "商家信息"
    obj= models.User.objects.filter(id=nid).first()
    if not obj:
        messages.error(req,"商家不存在！")
    name = obj.username
    form = models.Merchant.objects.filter(representative_name=name).first()
    return render(req,"user/list_content.html",{"form":form,"title":title})

#  审核商家
def me_status(req):
    uid = req.GET.get("uid")
    obj = models.User.objects.filter(id=uid).all()
    if not obj:
        return JsonResponse({
            "status": False,
            "error": "审核失败，数据出错",
        })  # JsonResponse返回状态Flase和错误
    models.User.objects.filter(id=uid).update(process=1)
    return JsonResponse({"status": True})


from ckeditor.fields import RichTextFormField
#  添加公告类
class Mess(BootsrapModel):
    content = RichTextFormField(label='内容',config_name = 'default')
    class Meta:
        model = models.Message
        fields= ['title','content']
#  添加公告
def mess_add(req):
    title = "添加公告"
    if req.method =='GET':
        form = Mess()
        content = {}
        content['form'] = form
        return render(req,"admin/ad_mess.html",content)
    form = Mess(data=req.POST)
    if form.is_valid():
        form.instance.name = req.session['info']['name']
        form.save()
        return redirect('/admin/mess/list/')
    content = {
        "title": title,
        "form": form,
    }
    return render(req, "admin/ad_mess.html", content)
#  公告列表
def mess_list(req):
    title = "公告列表"
    list = models.Message.objects.all()
    page_obj = Pagination(req, list)
    rid = req.session['info']['role_id']
    context = {
        "title": title,
        "list": page_obj.page_queryset,
        "page_string": page_obj.html(),
        "rid": rid,
    }
    return  render(req,"admin/message.html",context)

#  公告详情
def  mess_detail(req,nid):
    title = "公告详情"
    obj = models.Message.objects.filter(id=nid).first()
    return render(req,'user/list_content.html', {"obj": obj,"title":title})

def mess_edit(req,nid):
    title = "公告编辑"
    obj = models.Message.objects.filter(id=nid).first()
    if req.method == 'GET':
        form = Mess(instance=obj)
        return render(req,"admin/ad_mess.html",{"form":form,"title":title})
    form = Mess(data=req.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/admin/mess/list/')
    return  render(req,"admin/ad_mess.html",{"form":form,"title":title})

# 删除公告
def mess_del(req):
    id = req.GET.get('uid')
    exists = models.Message.objects.filter(id=id).exists()
    if not exists:
        return JsonResponse({
            "status": False,
            "error": "删除失败，数据不存在",
        })  # JsonResponse返回状态Flase和错误
    models.Message.objects.filter(id=id).delete()
    return JsonResponse({"status": True})



# # 搜素条件
# def adminlist(req):
#
#     # 检查用户是否已经登录
#     # 已登录，继续；未登录，跳转到登录页面
#     # 用户发来请求获取cookie随机字符串进行对比
#     # if not req.seesion.get["info"]:
#     #     return  redirect("/login/")
#     # info_dict = req.session["info"]
#     # print(info_dict["id"])
#     # print(info_dict["name"])
#     # 1
#     # 17387715045
#     # 搜素条件
#     data_list = {}
#     search_data = req.GET.get('data', "")
#     if search_data:
#         data_list["username__contains"] = search_data
#
#     queryset = models.Admin.objects.filter(**data_list)
#
#     #
#     page_object = Pagination(req, queryset)
#     context = {
#         "queryset": page_object.page_queryset,
#         "page_string": page_object.html(),
#         "search_data": search_data
#     }
#     return render(req, "admin_list.html", context)
#
#
# # 新建管理员
#
#
# def adminadd(req):
#     title = "新建管理员"
#     if req.method == "GET":
#         form = AdminModelForm()
#         return render(req, "form_add.html", {"form": form, "title": title})
#     form = AdminModelForm(data=req.POST)
#     if form.is_valid():
#         form.save()
#         return redirect("/admin/list")
#     return render(req, "form_add.html", {"form": form, "title": title})
#
# # 编辑管理员
#
#
# def adminupdate(req, nid):
#     title = "编辑管理员"
#     obj = models.Admin.objects.filter(id=nid).first()
#     if not obj:
#         return redirect("/admin/list/")
#     if req.method == "GET":
#         form = AdminUpadte(instance=obj)
#         return render(req, "form_add.html", {"form": form, "title": title})
#     form = AdminUpadte(data=req.POST, instance=obj)
#     if form.is_valid():
#         form.save()
#         return redirect("/admin/list")
#     return render(req, "form_add.html", {"form": form, "title": title})
#
# # 重置密码
#
#
# def adminpd(req, nid):
#     """重置密码"""
#     obj = models.Admin.objects.filter(id=nid).first()
#     if not obj:
#         return redirect("/admin/list/")
#     title = "重置密码-{}".format(obj.username)
#
#     if req.method == "GET":
#         form = Adminreset()
#         return render(req, "form_add.html", {"form": form, "title": title})
#     form = Adminreset(data=req.POST, instance=obj)
#     if form.is_valid():
#         form.save()
#         return redirect("/admin/list")
#     return render(req, "form_add.html", {"form": form, "title": title})
