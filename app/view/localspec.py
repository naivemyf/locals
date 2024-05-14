import json
from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # csrf用于Ajax
from app import models
# encoding:utf-8

#   特色分类页面
@csrf_exempt
def chocies(req):
    if req.method == 'GET':
        form = models.Choice.objects.all()
        return render(req,"user/favorite_choices.html", {"form": form})
    # 获取请求中的JSON数据
    filelist = req.POST.getlist('filelist')
    if not filelist :
        form = models.Choice.objects.all()
        mes = "请选择您的喜好"
        return   JsonResponse({"status": False,"mes":mes})
    my_dict = {item: 5 for item in filelist}
    user = req.session['account']
    models.Recommend.objects.create(user=user,score=my_dict)
    if filelist:
        return JsonResponse({"status":True})
    mes ="方法错误"
    return JsonResponse({"status": False,"mes":mes})
