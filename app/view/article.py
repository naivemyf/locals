from django.http import JsonResponse
from django.shortcuts import render, redirect
from app.utils.bootsrap import BootsrapModel, BootsrapForm
from app import models
from app.utils.form import ArticleAdd

# 文章添加
def articleadd(req):
    """文章添加"""
    title = "文章添加"
    if req.method == "GET":
        form = ArticleAdd()
        return render(req, "article.html", {'form': form, "title":title})
    form = ArticleAdd(data=req.POST)
    if form.is_valid():
        form.instance.username_id = req.session["info"]["id"]
        form.instance.status = 0
        form.instance.collect = 0
        form.save()
        return redirect('/article/listme/')
    return render(req, "article.html", {'form': form, "title":title})

# 文章列表
def list(req):
    """所有文章列表"""
    title = "文章列表"
    obj = models.Article.objects.filter(status=1).all()
    return render(req, "art_list.html", {'obj': obj, "title": title})

# 我的文章列表
def listme(req):
    """我的文章列表"""
    title= "我的文章列表"
    name = req.session["info"]["id"]
    obj = models.Article.objects.filter(username_id=name).all()
    return render(req, "art_list.html", {'obj': obj, "title": title})
# 文章详情
def art_detail(req,nid):
    """文章详情"""
    obj = models.Article.objects.filter(id=nid).first()
    if not obj:
        return redirect("article/listme")
    return render(req,"art_view.html", {"obj": obj})
# 文章编辑
def art_edit(req,nid):
    title = "文章编辑"
    obj = models.Article.objects.filter(id=nid).first()
    if req.method == "GET":
        form = ArticleAdd(instance=obj)
        return render(req, "article.html", {'form': form, "title":title})
    form = ArticleAdd(data=req.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('/article/listme/')
    return render(req, "article.html", {'form': form, "title":title})


# 删除文章
def art_delete(req):
    uid = req.GET.get("uid")
    exists = models.Article.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({
            "status": False,
            "error": "删除失败，数据不存在",
        })# JsonResponse返回状态Flase和错误
    models.Article.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})



