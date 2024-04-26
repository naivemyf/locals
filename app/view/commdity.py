import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from app.utils.bootsrap import BootsrapModel
from app import models
from django import forms
from django.views.decorators.csrf import csrf_exempt  # csrf用于Ajax
from django.contrib import  messages

# 商品添加类
class CommdityBootstrp(BootsrapModel):
    tag = forms.ModelChoiceField(queryset=models.Choice.objects.all(), empty_label="请选择标签")
    class Meta:
        model = models.Commdity  # 指定model数据库
        exclude = ["status","username","tag"]  # 排除不显示字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置pic字段不具有class属性
        if 'class' in self.fields['pic'].widget.attrs:
            del self.fields['pic'].widget.attrs['class']


@csrf_exempt
def commdityadd(req):
    title = "特产添加"
    if req.method == 'GET':
        form = CommdityBootstrp()
        return render(req, "commdity/comm_form.html", {"form": form,"title":title})
    form = CommdityBootstrp(data=req.POST)
    pic = req.FILES.get('pic')
    # req.session["pic"] = {
    #     'pic': pic
    # }
    if form.is_valid():
        form.instance.pic = pic
        form.instance.username = req.session["info"]["name"]
        form.instance.tag = req.cleaned_data["tag"]
        form.save()
        return redirect("/commdity/list/")
    # data_dict = {"status": False, 'error': form.errors}
    # return HttpResponse(json.dumps(data_dict, ensure_ascii=False))  # 返回状态Flase和错误
    return render(req,"commdity/comm_form.html",{"form": form,"title":title})
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
    list = models.Commdity.objects.filter(username=name).order_by("createtime")
    return render(req, "commdity/comm_mylist.html", {"title": title, "list": list})


# 商品列表（用户）
def commditylist(req):
    """商品列表"""
    title="商品列表"
    list = models.Commdity.objects.filter(status=1).all()
    return render(req, "commdity/comm_alllist.html", {"title": title, "list": list})

# 我的商品详情（商家）
def comm_detail(req,nid):
    title = "特产信息"
    uname = req.session["info"]["name"]
    obj= models.Commdity.objects.filter(id=nid).first()
    exists = models.Enshrine.objects.filter(username=uname ,comm_id=nid).exists()
    if exists:
        enshrine = models.Enshrine.objects.get(username=uname, comm_id=nid)
        ex_status = enshrine.status
        if ex_status ==0:
            exists = False
    if not obj:
        messages.error(req,"商品不存在！")
    return render(req,"user/list_content.html",{"obj":obj,"title":title,"exists":exists})


# 商品编辑（商家）
def comm_edit(req,nid):
    title = "商品编辑"
    obj = models.Commdity.objects.filter(id=nid).first()
    if req.method == "GET":
        form = CommdityBootstrp(instance=obj)
        return render(req, "commdity/comm_form.html", {'form': form, "title":title})
    form = CommdityBootstrp(data=req.POST, instance=obj)
    if form.is_valid():
        pic = req.FILES.get('pic')
        form.instance.pic = pic
        form.save()
        return redirect('/commdity/list/')
    return render(req, "commdity/comm_form.html", {'form': form, "title":title})

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

# 收藏商品
def comm_favorite(req,id):
    uname = req.session["info"]["name"]
    exists = models.Enshrine.objects.filter(username=uname,comm_id=id).exists()
    models.Enshrine.objects.filter(username=uname, comm_id=id).update(status=1)
    if not exists:
        model = models.Enshrine(username=uname, comm_id=id)
        model.save()
    return JsonResponse({'exists': exists})
# 取消收藏商品
def comm_fav_del(req,id):
    uname = req.session["info"]["name"]
    models.Enshrine.objects.filter(username=uname, comm_id=id).update(status=0)
    id_status = models.Enshrine.objects.get(username=uname, comm_id=id).status
    # 在收藏表中获取取消商品的状态
    if id_status == 0:
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

