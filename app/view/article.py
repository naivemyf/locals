from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from app.utils.bootsrap import BootsrapModel, BootsrapForm
from app import models
from app.utils.form import ArticleAdd,ArticleEdit
from app.utils.pagination import Pagination
from app.utils.sensitivewords import SensitiveFilter
# 文章添加
def articleadd(req):
    """文章添加"""
    title = "文章添加"
    if req.method == "GET":
        form = ArticleAdd()
        return render(req, "article/article.html", {'form': form, "title":title})
    form = ArticleAdd(data=req.POST)
    res = None
    if form.is_valid():
        form.instance.username = req.session["info"]["name"]
        form.instance.status = 1
        form.instance.collect = 0
        form.instance.tag = form.cleaned_data["tag"]
        str = form.cleaned_data['content']
        Filter = SensitiveFilter()
        res = Filter.replaceSensitive(txt=str)
        if res:
            return render(req, "article/article.html", {'form': form, "title": title, "res": res})
        form.save()
        return redirect('/article/listme/')
    return render(req, "article/article.html", {'form': form, "title":title})

# 文章列表
def list(req):
    """所有文章列表"""
    title = "文章列表"
    obj = models.Article.objects.filter(status=2).all()
    page_obj = Pagination(req, obj)
    context = {
        "title": title,
        "list": page_obj.page_queryset,
        "page_string": page_obj.html()
    }
    return render(req, "article/art_list.html", context)

# 我的文章列表
def listme(req):
    """我的文章列表"""
    title= "我的文章列表"
    name = req.session["info"]["name"]
    obj = models.Article.objects.filter(username=name).all()
    page_obj = Pagination(req, obj)
    context = {
        "title": title,
        "obj": page_obj.page_queryset,
        "page_string": page_obj.html()
    }
    return render(req, "article/art_list.html", context)


# 文章详情
def art_detail(req,nid):
    """文章详情"""
    title = "文章信息"
    uname = None
    rid = None
    info = req.session.get('info', None)
    if info:
        uname =info.get('name')
    exists = models.User.objects.filter(username=uname).exists()
    if exists:
        rid = models.User.objects.get(username=uname)
        rid = rid.role.id
    obj = models.Article.objects.filter(id=nid).first()
    exists = models.Enshrine.objects.filter(username=uname, art_id=nid).exists()
    if exists:
        enshrine = models.Enshrine.objects.get(username=uname, art_id=nid)
        ex_status = enshrine.status
        if ex_status == 0:
            exists = False
    if not obj:
        return redirect("article/listme")
    return render(req,"user/list_content.html", {"obj": obj,"title":title,"exists":exists,"rid":rid})

# 文章编辑
def art_edit(req,nid):
    title = "文章编辑"
    obj = models.Article.objects.filter(id=nid).first()
    if req.method == "GET":
        form = ArticleEdit(instance=obj)
        return render(req, "article/article.html", {'form': form, "title":title})
    form = ArticleEdit(data=req.POST, instance=obj)
    if form.is_valid():
        form.instance.status = 0
        tag = str(form.cleaned_data["select_tag"])
        if tag == 'None':
            form.save()
            return redirect('/article/listme/')
        form.instance.tag =tag
        form.save()
        return redirect('/article/listme/')
    return render(req, "article/article.html", {'form': form, "title":title})


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

# 收藏文章
def art_favorite(req,id):
    uname = req.session["info"]["name"]
    exists = models.Enshrine.objects.filter(username=uname,art_id=id).exists()
    models.Enshrine.objects.filter(username=uname, art_id=id).update(status=1)
    if not exists:
        model = models.Enshrine(username=uname, art_id=id)
        model.save()
    return JsonResponse({'exists': exists})

# 取消收藏文章
def art_fav_del(req,id):
    uname = req.session["info"]["name"]
    models.Enshrine.objects.filter(username=uname, art_id=id).update(status=0)
    id_status = models.Enshrine.objects.get(username=uname, art_id=id).status
    # 在收藏表中获取取消商品的状态
    if id_status == 0:
        return JsonResponse({"status": True})
    return JsonResponse({"status": False})

# 我的文章收藏
def art_fav_list(req):
    title = "我的文章收藏"
    uname = req.session["info"]["name"]
    list = models.Enshrine.objects.filter(username=uname,status=1).all()
    return render(req,"user/list_content.html", {"list": list, "title": title})



