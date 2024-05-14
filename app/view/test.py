import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from app.utils.bootsrap import BootsrapModel
from app import models
from django import forms
from django.views.decorators.csrf import csrf_exempt  # csrf用于Ajax
from django.contrib import  messages
@csrf_exempt
class CommdityBootstrp(BootsrapModel):
    class Meta:
        model = models.Choice  # 指定model数据库
        fields = "__all__"  # 指定字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置pic字段不具有class属性
        if 'class' in self.fields['pic'].widget.attrs:
            del self.fields['pic'].widget.attrs['class']



def add(req):
    title = "特产添加"
    if req.method == 'GET':
        form = CommdityBootstrp()
        return render(req, "user/aaa.html", {"form": form,"title":title})
    form = CommdityBootstrp(data=req.POST)
    pic = req.FILES.get('pic')
    # req.session["pic"] = {
    #     'pic': pic
    # }
    if form.is_valid():
        form.instance.pic = pic
        # form.instance.username = req.session["info"]["name"]
        form.save()
        return redirect("/index/")
    # data_dict = {"status": False, 'error': form.errors}
    # return HttpResponse(json.dumps(data_dict, ensure_ascii=False))  # 返回状态Flase和错误
    return render(req,"user/aaa.html",{"form": form,"title":title})