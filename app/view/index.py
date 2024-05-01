from django.shortcuts import render, redirect
from app.view.user_recommd import generate_user_enshrine_tag_count, recommend, top_recommed, most_list
# encoding:utf-8
import sys
from app import models
import ast
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt  # csrf用于Ajax


def index(req):
    account = req.session.get('account', None)
    # 注册session名字
    info = req.session.get('info', None)
    #  登录session名字
    name = None
    exists = False
    if account:  # 如果用户进行注册，查找用户是否进行特色选择
        name = account
        exists = models.Recommend.objects.filter(user=name).exists()
    elif info:  # 判断登录用户是否选择过特色
        name = info.get('name')
        exists = models.Recommend.objects.filter(user=name).exists()
    if exists:   # 如果存在特色选择，就在返回选择的对象
        va = models.Recommend.objects.get(user=name).score
        data = ast.literal_eval(va)  # 将字符串转换为字典
        dict = defaultdict(int)  # 创建一个默认字典
        for key, value in data.items():
            dict[key] += int(value)  # 将数据对象字典的所有转存在默认字典
        if dict:  # 如果默认字典不为空
            nested_dict = {}  # 创建一个嵌套字典
            nested_dict[name] = dict  # 将默认字典添加到嵌套字典
            all_tag_count = generate_user_enshrine_tag_count()  # 实列用户标签字典
            new_dict(nested_dict, all_tag_count)  # 实列添加目标用户后的用户标签字典
            res = recommend(name, nested_dict)  # 实列推荐算法
            req.session['account'] = ''  # 清空account的内容
            rec_list = indexhtml(res)  # 推荐文章和特色商品的值进行百分比计数，后返回相应的篇数
            tag = models.Choice.objects.all()
            return render(req, "user/index.html", {"rec_list": rec_list, "tag": tag})
    else:
        count = models.Enshrine.objects.filter(username=name).count()
        if count > 10:
            res = most_list(name)
            rec_list = indexhtml(res)
            tag = models.Choice.objects.all()
            return render(req, 'user/index.html', {"rec_list": rec_list, "tag": tag})
        else:
            top_rec = top_recommed()  # 实列前二十推荐
            art_list = []
            comm_list = []
            for i in top_rec[0]:
                art_list += models.Article.objects.filter(id=i).all()
            for i in top_rec[1]:
                comm_list += models.Commdity.objects.filter(id=i).all()
            rec_list = {
                'art': art_list,
                'comm': comm_list,
            }
            tag = models.Choice.objects.all()
            return render(req, "user/index.html", {"rec_list": rec_list, "tag": tag})

#  合并字典
def new_dict(dict1, dict2):
    """合并字典"""
    for key, value in dict2.items():
        if key in dict1:
            dict1[key].update(value)
        else:
            dict1[key] = value
    return dict1

# 计算标签占比
def indexhtml(res):
    rec_list = res[0]
    # 计算所有标签值的总和
    total = sum([x[1] for x in rec_list])
    comm_list = []
    art_list = []
    # 计算每个标签的占比并四舍五入取整
    percent = [(x[0], round(x[1] / total * 10)) for x in rec_list]
    for i in percent:
        comm_list += models.Commdity.objects.filter(tag=i[0])[:i[1] * 2]
        art_list += models.Article.objects.filter(tag=i[0])[:i[1] * 2]
        rec_list = {
            'art': art_list,
            'comm': comm_list,
        }
    return rec_list

# 标题列表
def tag(req,nid):
    tag = models.Choice.objects.filter(id=nid).first()
    tag = tag.name
    tag_art = models.Article.objects.filter(tag=tag).all()
    tag_comm = models.Commdity.objects.filter(tag=tag).all()
    content ={
        "tag":tag,
        "tag_art":tag_art,
        "tag_comm":tag_comm
    }
    return render(req,"user/tag_list.html",{"content":content})