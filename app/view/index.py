from django.shortcuts import render, redirect
from app.view.user_recommd import generate_user_enshrine_tag_count,recommend,top_recommed
# encoding:utf-8
import sys


def index(req):
    name = req.session['info']['name']
    value = req.session['select']['score_insterest']
    if value:
        nested_dict ={}
        nested_dict[name] = value
        all_tag_count=generate_user_enshrine_tag_count()  # 实列用户标签字典
        new_dicta = new_dict(nested_dict, all_tag_count)  # 实列添加目标用户后的用户标签字典
        res = recommend(name, new_dicta)
        rec_list=res[0]
        rec_top =res[1]
        top_rec = top_recommed();
        return render(req, "user/index.html",{"res":res})
    else:
        return render(req,"user/index.html")

def new_dict(dict1,dict2):
    for key, value in dict2.items():
        if key in dict1:
            dict1[key].update(value)
        else:
            dict1[key] = value
    return dict1
