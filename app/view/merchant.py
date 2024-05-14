from django.http import HttpResponse
from django.shortcuts import render,redirect

from app import models
from app.utils.form import LoginForm


def login(req):
    """登录"""
    if req.method == "GET":
        form = LoginForm()
        return render(req, 'merchant/me_login.html', {'form': form})

    form = LoginForm(data=req.POST)
    if form.is_valid():
        # 验证成功,获取用户名和密码
        #print(form.cleaned_data) 打印加密后的值
        # 获取的值
        # {'username': 'xxxx', 'password':‘xxxxxxxxxxxxxxxx'}
        # form.cleaned_data["code"]
        # 将输入的验证码从框架获取数据的字典中删除

        # 验证码校验
        user_input_code = form.cleaned_data.pop("code")
        code = req.session.get("image_code", "")
        if code.upper() != user_input_code:
            form.add_error("code", "验证码错误")
            return render(req, "merchant/me_login.html", {"form": form})

        # 数据库检验用户名和密码
        # models.Admin.objects.filter(username='form.cleaned_data['username']',password='form.cleaned_data['password']').first()
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或者密码错误！")  # 显示错误信息在password框下面
            return render(req, 'merchant/me_login.html', {'form': form})

        # 网站生成随机字符串，写到用户浏览器的cookie和session中
        req.session["info"] = {
            'id': admin_object.id,
            'name': admin_object.username,
            "role_id": admin_object.role_id}
        # 七天免登录
        req.session.set_expiry(60 * 60 * 24 * 7)

        rid = admin_object.role_id
        if  rid == 2 and admin_object.process == 0:#未审核商家
            return HttpResponse('<p style="text-align:center;font-size: 60px">注册成功，请等待管理员审核<p>')
        elif rid == 2 and admin_object.process == 1:#已审核商家
            return redirect("/merchant/")
    return render(req, 'merchant/me_login.html', {'form': form})

def merchantindex(req):
    cname= req.session["info"]["name"]
    comm_counts = models.Commdity.objects.filter(username=cname).count()
    ad_comm = models.Commdity.objects.filter(username=cname, status=1).count()
    unad_comm = models.Commdity.objects.filter(username=cname, status=0).count()
    data ={
        "comm_counts": comm_counts,
        "ad_comm": ad_comm,
        "unad_comm": unad_comm
    }
    comm = models.Commdity.objects.filter(username=cname, status=1).all()
    comm_list = []
    for i in comm:
        if i.message:
            comm_dict = {
                "id": i.id,
                "mes": i.message,
                "time": i.timemes,
                "title": i.title,
                "createtime": i.timestamp,
            }
            comm_list.append(comm_dict)
    return render(req, 'merchant/merchant.html', { "comm": comm_list,"data": data})


