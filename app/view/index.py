from django.shortcuts import render, redirect
from app.view.user_recommd import generate_user_enshrine_tag_count, recommend
from app.view.user_recommd import top_recommed,most_list,random_list

# encoding:utf-8
import sys
from app import models
import ast
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt  # csrf用于Ajax


# top_rec = top_recommed()  # 实列前二十推荐
#             if top_rec[0] and top_rec[1]:  # 判断推荐文章和特色商品是否为空
#                 art_list = []
#                 comm_list = []
#                 for i in top_rec[0]:
#                     art_list += models.Article.objects.filter(id=i).all()
#                 for i in top_rec[1]:
#                     comm_list += models.Commdity.objects.filter(id=i).all()
#                 rec_list = {
#                     'art': art_list,
#                     'comm': comm_list,
#                 }
#                 tag = models.Choice.objects.all()
#                 return render(req, "user/index.html", {"rec_list": rec_list, "tag": tag})

def index(req):
    dict = {}
    nested_dict = {}  # 创建字典
    resa = None
    resb = None
    res = []
    info = req.session.get('info', None)
    #  登录session名字
    tag = models.Choice.objects.all()
    if info:
        name = info.get('name')
        all_tag_count = generate_user_enshrine_tag_count()  # 实列用户标签字典
        exists = models.Recommend.objects.filter(user=name).exists()  # 判断用户兴趣分类
        if exists:  # 用户兴趣分类存在
            va = models.Recommend.objects.get(user=name).score  # 获取用户的兴趣字段
            data = ast.literal_eval(va)  # 将字符串转换为字典
            dict = defaultdict(int)  # 创建一个字典
            for key, value in data.items():
                dict[key] += int(value)  # 将数据对象转存在默认字典
        if dict:  # 如果默认字典不为空
            nested_dict[name] = dict  # 将默认字典添加到嵌套字典
        if all_tag_count:
            new_dict(nested_dict, all_tag_count)  # 实列添加目标用户后的用户标签字典
            a = 0
            for key in nested_dict.items():
                a += 1
                if a >= 3:
                    resa = recommend(name, nested_dict)  # 实列推荐算法
        count = models.Enshrine.objects.filter(username=name).count()
        if count > 10:  # 判断用户收藏数量
            resb = most_list(name)
        if resa and resb: # 判断用户兴趣分类存在和用户收藏是否存在
            res = resa[0] + resb[0]  # 将推荐算法和最多收藏的文章和商品进行合并
            result = {}
            for item in res:
                if item[0] in result:
                    result[item[0]] += item[1]
                else:
                    result[item[0]] = item[1]
            res = tuple(result.items())
        elif not resa and resb:  # 判断用户兴趣分类存在
            res = resb[0]
        elif not resb and resa:  # 判断用户收藏数量
            res = resa[0]
        if res:
            rec_list = indexhtml(res)
            return render(req, "user/index.html", {"rec_list": rec_list, "tag": tag})
        else:
            lista = random_list()  # 随机推荐
            if lista:
                art_list = []
                comm_list = []
                for i in lista['art_ids']:
                    art_list += models.Article.objects.filter(id=i).all()
                for i in lista['comm_ids']:
                    comm_list += models.Commdity.objects.filter(id=i).all()
                rec_list = {
                    'art': art_list,
                    'comm': comm_list,
                }
                tag = models.Choice.objects.all()
                return render(req, "user/index.html", {"rec_list": rec_list, "tag": tag})
    else:
        lista = random_list() # 随机推荐
        if lista:
            art_list = []
            comm_list = []
            for i in lista['art_ids']:
                art_list += models.Article.objects.filter(id=i).all()
            for i in lista['comm_ids']:
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
    rec_list = res
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