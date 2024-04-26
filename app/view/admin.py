# from app.utils.pagination import Pagination
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from app import models
from django import forms
from app.utils.bootsrap import BootsrapModel
# from app.utils.form import Adminreset, AdminUpadte, AdminModelForm


def adminindex(req):
    art_counts = models.Article.objects.filter(status=0).count()
    comm_counts = models.Commdity.objects.filter(status=0).count()
    me_counts = models.User.objects.filter(process=0).count()
    data={
        "art_counts": art_counts,
        "comm_counts": comm_counts,
        "me_counts": me_counts
    }
    return render(req, "admin/admin.html", {"data": data})


class Ad_art(BootsrapModel):
    class Meta:
        form = models.Article
        fields = "__all__"

#  未审核文章列表
def ad_art_list_no(req):
    """未审核文章列表"""
    title='未审核文章'
    art_list = models.Article.objects.filter(status=0).all()
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

#  批量审核文章
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

#  审核文章
def art_status(req):
    uid = req.GET.get("uid")
    obj = models.Article.objects.filter(id=uid).first()
    if not obj:
        return JsonResponse({
            "status": False,
            "error": "审核失败，数据出错",
        })  # JsonResponse返回状态Flase和错误
    models.Article.objects.filter(id=uid).update(status=1)
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
            models.Article.objects.filter(id=uid).update(status=1)
        return JsonResponse({'status': True})

#  审核商家
def me_status(req):
    uid = req.GET.get("uid")
    obj = models.User.objects.filter(id=uid).first()
    if not obj:
        return JsonResponse({
            "status": False,
            "error": "审核失败，数据出错",
        })  # JsonResponse返回状态Flase和错误
    models.User.objects.filter(id=uid).update(process=1)
    return JsonResponse({"status": True})
#
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
