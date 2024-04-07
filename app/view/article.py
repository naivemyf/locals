from django.shortcuts import render, redirect
from app.utils.bootsrap import BootsrapModel, BootsrapForm
from app import models
from app.utils.form import ArticleAdd
# 文章添加
def articleadd(req):
    """文章添加"""
    if req.method == "GET":
        form = ArticleAdd()
        return render(req, "article.html", {'form': form})
    form = ArticleAdd(data=req.POST)
    if form.is_valid():
        form.instance.username_id = req.session["info"]["id"]
        form.instance.status = 0
        form.instance.collect = 0
        form.save()
        return redirect('/article/list/')
    return render(req, "article.html", {'form': form})

# 文章列表
def list(req):
    """所有文章列表"""
    title = "文章列表"
    obj = models.Article.objects.all()
    return render(req, "articleList.html", {'obj': obj, "title": title})

# 我的文章列表
def listme(req):
    """我的文章列表"""
    title= "我的文章列表"
    name = req.session["info"]["id"]
    obj = models.Article.objects.filter(username_id=name).all()
    return render(req, "articleList.html", {'obj': obj, "title": title})





