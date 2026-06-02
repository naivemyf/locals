"""
公共认证工具 —— 抽取 account / admin / merchant 中重复的登录逻辑。
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app import models


def handle_login(req, form_class, template_name, role_router):
    """
    通用登录处理函数。

    :param req:         Django HttpRequest 对象
    :param form_class:  LoginForm 类
    :param template_name: 登录页面模板路径
    :param role_router: 函数 (admin_object, req) -> HttpResponse 或 None
                        根据角色返回重定向 / 错误响应；返回 None 则重新渲染表单。
    :return:            HttpResponse
    """
    if req.method == "GET":
        form = form_class()
        return render(req, template_name, {"form": form})

    form = form_class(data=req.POST)
    if not form.is_valid():
        return render(req, template_name, {"form": form})

    # 验证码校验
    user_input_code = form.cleaned_data.pop("code")
    code = req.session.get("image_code", "")
    if code.upper() != user_input_code:
        form.add_error("code", "验证码错误")
        return render(req, template_name, {"form": form})

    # 数据库校验
    admin_object = models.User.objects.filter(**form.cleaned_data).first()
    if not admin_object:
        form.add_error("password", "用户名或者密码错误！")
        return render(req, template_name, {"form": form})

    # 写入 session
    req.session["info"] = {
        "id": admin_object.id,
        "name": admin_object.username,
        "role_id": admin_object.role_id,
    }
    req.session.set_expiry(60 * 60 * 24 * 7)  # 七天免登录

    # 委托角色路由
    result = role_router(admin_object, req)
    if result is not None:
        return result
    return render(req, template_name, {"form": form})
