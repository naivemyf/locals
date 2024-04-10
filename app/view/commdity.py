import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from app.utils.bootsrap import BootsrapModel
from app import models
from django.views.decorators.csrf import csrf_exempt  # csrf用于Ajax
from django.contrib import  messages

# 商品添加类
class CommdityBootstrp(BootsrapModel):
    class Meta:
        model = models.Commdity  # 指定model数据库
        exclude = ["status","username"]  # 排除不显示字段

@csrf_exempt
def commdityadd(req):
    title = "商品添加"
    if req.method == 'GET':
        form = CommdityBootstrp()
        return render(req, "comm_form.html", {"form": form,"title":title})
    form = CommdityBootstrp(data=req.POST)
    pic = req.FILES.get('pic')
    # req.session["pic"] = {
    #     'pic': pic
    # }
    if form.is_valid():
        form.instance.pic = pic

        form.instance.username = req.session["info"]["name"]

        form.save()
        return redirect("/merchant/")
    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))  # 返回状态Flase和错误

# 商品所有字段类
class CommdityListForm(BootsrapModel):
    """我的商品列表类"""
    class Meta:
        model = models.Commdity
        fields = "__all__"



# 商品列表（商家）
def commditylistme(req):
    """我的商品列表"""
    title="我发布的商品"
    name = req.session["info"]["name"]
    form =CommdityListForm()
    list = models.Commdity.objects.filter(username=name).all()
    return render(req, "comm_mylist.html", {"title": title, "list": list})


# 商品列表（用户）
def commditylist(req):
    """商品列表"""
    title="商品列表"
    form =CommdityListForm()
    list = models.Commdity.objects.filter(status=1).all()
    return render(req, "comm_alllist.html", {"title": title, "list": list})

# 我的商品详情（商家）
def comm_detail(req,nid):
    title = "我的商品详情"
    obj= models.Commdity.objects.filter(id=nid).first()
    if not obj:
        messages.error(req,"商品不存在！")
    return render(req,"comm_view.html",{"obj":obj,"title":title})

# 商品详情（用户）
def comm_all_detail(req,nid):
    title = "商品详情"
    obj= models.Commdity.objects.filter(id=nid).first()
    if not obj:
        messages.error(req,"商品不存在！")
    return render(req,"comm_view.html",{"obj":obj,"title":title})

# 商品编辑（商家）
def comm_edit(req,nid):
    title = "文章编辑"
    obj = models.Commdity.objects.filter(id=nid).first()
    if req.method == "GET":
        form = CommdityBootstrp(instance=obj)
        return render(req, "comm_form.html", {'form': form, "title":title})
    form = CommdityBootstrp(data=req.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/commdity/list/')
    return render(req, "comm_form.html", {'form': form, "title":title})

# 删除商品（商家）
def comm_delete(req):
    uid = req.GET.get("uid")
    exists = models.Commdity.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({
            "status": False,
            "error": "删除失败，数据不存在",
        })# JsonResponse返回状态Flase和错误
    models.Commdity.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})


