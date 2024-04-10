# from app.utils.pagination import Pagination
from django.shortcuts import render, redirect
from app import models
from app.utils.bootsrap import BootsrapModel
# from app.utils.form import Adminreset, AdminUpadte, AdminModelForm


def adminindex(req):
    return render(req, "admin.html")


class Ad_art(BootsrapModel):
    class Meta:
        form = models.Article
        fields = "__all__"

# 文章列表
def ad_art_list_no(req):
    """未审核文章列表"""
    title='未审核文章'
    art_list = models.Article.objects.filter(status=0).all()
    return render(req,"ad_art_list.html", {'art_list': art_list, "title": title})

def ad_art_list(req):
    """所有文章列表"""
    title = '所有文章'
    art_list = models.Article.objects.all()
    return render(req,"ad_art_list.html", {'art_list': art_list, "title": title})


# 商家
def ad_me_listno(req):
    """未审核商家列表"""
    title = '未审核商家'
    me_list = models.User.objects.filter(process=0).all()
    return render(req, "ad_me_list.html", {'me_list': me_list, "title": title})

def ad_me_list(req):
    """未审核商家列表"""
    title = '所有商家'
    me_list = models.User.objects.filter(role=2).all()
    return render(req, "ad_me_list.html", {'me_list': me_list, "title": title})

# 商品
def ad_comm_listno(req):
    title = "未审核商品"
    comm_list = models.Commdity.objects.filter(status=0).all()
    return render(req, "ad_comm_list.html", {"title": title, "comm_list": comm_list})

def ad_comm_list(req):
    title = "所有商品"
    comm_list = models.Commdity.objects.all()
    return  render(req, "ad_comm_list.html", {"title": title, "comm_list": comm_list})
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
