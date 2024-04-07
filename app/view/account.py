from io import BytesIO
from django.shortcuts import render, HttpResponse, redirect
from app import models
from app.utils.code import check_code
from app.utils.form import RegisterForm, LoginForm




#注册
def register(req):
    #"""注册"""
    if req.method == "GET":
        form = RegisterForm()
        return render(req, 'register.html', {'form': form})
    form = RegisterForm(data=req.POST)
    if form.is_valid():
        role = form.cleaned_data.get("role").id
        if role == 1:
            form.save()
            return redirect("/login/")
        elif role == 2:
            form.instance.process =0
            form.save()
            return HttpResponse('<p style="text-align:center;font-size: 60px">注册成功，请等待管理员审核<p>')
        elif role == 3:
            return HttpResponse('<p style="text-align:center;font-size: 60px">管理员无需注册<p>')
    return render(req, 'register.html', {'form': form})
# 登录
def login(req):
    """登录"""
    if req.method == "GET":
        form = LoginForm()
        return render(req, 'login.html', {'form': form})

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
        # if code.upper() != user_input_code:
        #     form.add_error("code", "验证码错误")
        #     return render(req, "login.html", {"form": form})

        # 数据库检验用户名和密码
        # models.Admin.objects.filter(username='form.cleaned_data['username']',password='form.cleaned_data['password']').first()
        admin_object = models.User.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password", "用户名或者密码错误！")  # 显示错误信息在password框下面
            return render(req, 'login.html', {'form': form})

        # 网站生成随机字符串，写到用户浏览器的cookie和session中
        req.session["info"] = {
            'id': admin_object.id,
            'name': admin_object.username,
            "role_id": admin_object.role_id}
        # 七天免登录
        req.session.set_expiry(60 * 60 * 24 * 7)
        rid = admin_object.role_id
        if rid == 1:#普通使用者
            return redirect('/index/')#信息正确，跳转首页
        elif rid == 2 and admin_object.process == 0:#未审核商家
            return HttpResponse('<p style="text-align:center;font-size: 60px">注册成功，请等待管理员审核<p>')
        elif rid == 2 and admin_object.process == 1:#已审核商家
            return redirect("/merchant/")
        elif rid == 3:#管理员
            return redirect("/index/")
    return render(req, 'login.html', {'form': form})

# 生成验证码
def image_code(req):
    """生成验证码"""
    img, code = check_code()
    # 写入session，以便验证
    req.session["image_code"] = code
    # session设置60秒超时
    req.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())#返回图片

# 注销
def logout(req):
    """注销"""
    req.session.clear()
    return redirect("/index/")
