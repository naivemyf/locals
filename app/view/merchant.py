from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django import forms
from app import models
from app.utils.encrypt import md5
from app.utils.form import LoginForm
from app.utils.bootsrap import BootsrapModel, BootsrapForm
from app.utils.auth_utils import handle_login

class RegisterForm(BootsrapModel):

    contact_phone=forms.CharField(
        label="电话号码",
        widget=forms.TextInput,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误'), ],
        required=True
    )
    id_number = forms.CharField(
        label="法人身份证号码",
        widget=forms.TextInput,
        validators=[RegexValidator(r'^(\d{15}|\d{17}[0-9Xx])$', '身份证号码格式错误'),],
        required=True
    )
    fpassword = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    class Meta:
        model =models.Merchant
        fields = ["company_name","company_type", "representative_name", "id_number", "id_expiration_date",
                  "contact_phone","actual_office_address","password","fpassword"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_phonenumber(self):  # 钩子函数
        txt_moblie = self.cleaned_data.get("phonenumber")# 获取用户填写的号码
        exists = models.User.objects.filter(
            phonenumber=txt_moblie).exists()  # 通过数据库查询新号码是否存在
        if exists:  # 如果号码存在，提示号码存在
            raise ValidationError("手机号码存在")
        return txt_moblie

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_fpassword(self):
        pwd = self.cleaned_data.get("password")
        verify_pwd = self.cleaned_data.get("fpassword")
        if pwd != md5(verify_pwd):
            raise ValidationError("密码错误！请重新输入")
        return verify_pwd

class User(BootsrapForm):
    class Meta:
        models = models.User
        fields = "__all__"
def register(req):
    if req.method == "GET":
        form = RegisterForm()
        return render(req, 'merchant/register.html', {'form': form})
    form = RegisterForm(data=req.POST)
    if form.is_valid():
        req.session["account"] = form.cleaned_data.get("representative_name")
        user = models.User()
        user.username = form.cleaned_data.get("representative_name")
        user.password = form.cleaned_data.get("password")
        user.phonenumber = form.cleaned_data.get("contact_phone")
        user.process = 0
        user.role_id = 2
        user.save()
        form.save()
        return redirect("/merchant/login")
    return render(req, 'merchant/register.html', {'form': form})
def login(req):
    """商家登录"""
    def merchant_router(admin_object, _req):
        if admin_object.role_id == 2 and admin_object.process == 0:  # 未审核商家
            return HttpResponse('<p style="text-align:center;font-size: 60px">注册成功，请等待管理员审核<p>')
        elif admin_object.role_id == 2 and admin_object.process == 1:  # 已审核商家
            return redirect("/merchant/")
        return None

    return handle_login(req, LoginForm, "merchant/me_login.html", merchant_router)

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


