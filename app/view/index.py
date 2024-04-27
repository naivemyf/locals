from django.shortcuts import render, redirect
from app.view.user_recommd import generate_user_enshrine_tag_count,recommend,top_recommed
# encoding:utf-8
import sys
from  app import models
import ast
from collections import defaultdict

def index(req):
    req.session['account'] = 'a15'
    account = req.session.get('account', None)
    # 注册session名字
    info = req.session.get('info', None)
    #  登录session名字
    name = None
    exists = False
    if account:
        name = account
        exists = models.Recommend.objects.filter(user=name).exists()

    elif info:
        name =info.get('name')
        exists = models.Recommend.objects.filter(user=name).exist()

    if exists:
        va = models.Recommend.objects.get(user=name).score
        data = ast.literal_eval(va)
        dict = defaultdict(int)
        for key,value in data.items():
            dict[key] += int(value)
        if dict:
            nested_dict ={}
            nested_dict[name] = dict
            all_tag_count=generate_user_enshrine_tag_count()  # 实列用户标签字典
            new_dict(nested_dict, all_tag_count)  # 实列添加目标用户后的用户标签字典
            res = recommend(name, nested_dict)
            top_rec = top_recommed()
            # req.session['account'] = ''
            #  清空account的内容
            a =req.session['account']
            percent = indexhtml(res)
            return render(req, "user/index.html",{"percent":percent})
    else:
        return render(req,"user/index.html")

#  合并字典
def new_dict(dict1,dict2):
    """合并字典"""
    for key, value in dict2.items():
        if key in dict1:
            dict1[key].update(value)
        else:
            dict1[key] = value
    return dict1

def indexhtml(res):
    rec_list = res[0]
    rec_name = res[1]
    # 计算所有标签值的总和
    total = sum([x[1] for x in rec_list])

    # 计算每个标签的占比并四舍五入取整
    percent = [(x[0], round(x[1] / total * 10)) for x in rec_list]
    for i in percent:
        comm_list = models.Commdity.objects.filter(tag=i[0])[:i[1]]
        art_list = models.Article.objects.filter(tag=i[0])[:i[1]]

    return percent



