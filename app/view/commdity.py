from django.shortcuts import render,redirect
from app.utils.bootsrap import BootsrapModel
from app import models
from app.utils.uploads import getNewName
from django.conf import settings
from django.http import HttpResponse, JsonResponse


class CommdityBootstrp(BootsrapModel):
    class Meta:
        model = models.Commdity  # 指定model数据库
        exclude= ["status","pic","username"]  # 排除不显示字段


def insertProductData(request):
    model = models.Commdity.objects
    # 获取上传文件的处理对象
    pic = request.FILES.get('pic')
    try:
        # 创建插入
        model.create(
            name=request.POST.get("name"),
            code=request.POST.get("code"),
            pic=pic,
            purchase_price=request.POST.get("purchase_price"),
            sole_price=request.POST.get("sole_price"),
        )
        context = {'info': '添加成功！'}
    except Exception as res:
        print(res)
        context = {'info': res}
    return JsonResponse({"msg": context})

def commdityadd(req):
    if req.method == 'GET':
        form = CommdityBootstrp()
        return render(req, "commdity.html", {"form": form})
    form = CommdityBootstrp(data=req.POST)
    if form.is_valid():
        form.save()
        return redirect("/merchant/")
    return render(req, 'commdity.html', {"form": form})

def commditylist(req):
    return render(req, "commdityList.html")

