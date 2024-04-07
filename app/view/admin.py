# from app.utils.pagination import Pagination
from django.shortcuts import render, redirect
from app import models
from app.utils.bootsrap import BootsrapModel
# from app.utils.form import Adminreset, AdminUpadte, AdminModelForm

def adminindex(req):
    return render(req, "admin.html")

# 搜素条件
def adminlist(req):

    # 检查用户是否已经登录
    # 已登录，继续；未登录，跳转到登录页面
    # 用户发来请求获取cookie随机字符串进行对比
    # if not req.seesion.get["info"]:
    #     return  redirect("/login/")
    # info_dict = req.session["info"]
    # print(info_dict["id"])
    # print(info_dict["name"])
    # 1
    # 17387715045
    # 搜素条件
    data_list = {}
    search_data = req.GET.get('data', "")
    if search_data:
        data_list["username__contains"] = search_data

    queryset = models.Admin.objects.filter(**data_list)

    #
    page_object = Pagination(req, queryset)
    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data
    }
    return render(req, "admin_list.html", context)


# 新建管理员


def adminadd(req):
    title = "新建管理员"
    if req.method == "GET":
        form = AdminModelForm()
        return render(req, "form_add.html", {"form": form, "title": title})
    form = AdminModelForm(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(req, "form_add.html", {"form": form, "title": title})

# 编辑管理员


def adminupdate(req, nid):
    title = "编辑管理员"
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect("/admin/list/")
    if req.method == "GET":
        form = AdminUpadte(instance=obj)
        return render(req, "form_add.html", {"form": form, "title": title})
    form = AdminUpadte(data=req.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(req, "form_add.html", {"form": form, "title": title})

# 重置密码


def adminpd(req, nid):
    """重置密码"""
    obj = models.Admin.objects.filter(id=nid).first()
    if not obj:
        return redirect("/admin/list/")
    title = "重置密码-{}".format(obj.username)

    if req.method == "GET":
        form = Adminreset()
        return render(req, "form_add.html", {"form": form, "title": title})
    form = Adminreset(data=req.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list")
    return render(req, "form_add.html", {"form": form, "title": title})
