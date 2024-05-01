from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from app import models
from app.utils.bootsrap import BootsrapForm,BootsrapModel
from app.utils.encrypt import md5

# 数据库中拿字段
# class LoginModelForm(forms.ModelForm):
#     class Meta:
#         model =models.Admin
#         fields =['username']

#注册类(Model从数据库拿取字段)
class RegisterForm(BootsrapModel):

    phonenumber=forms.CharField(
        label="电话号码",
        widget=forms.TextInput,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号码格式错误'), ],
        required=True
    )
    fpassword = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    # role = forms.ModelChoiceField(
    #     label="角色",
    #     queryset=models.Role.objects.all()[:2],
    #     required=True
    # )

    class Meta:
        model =models.User
        fields = ["username", "phonenumber", "password", "fpassword", "role"]
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

# 登录类
# 自定义(没有关联数据库)
class LoginForm(BootsrapForm):
    phonenumber = forms.CharField(
        label="账号",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True  # 默认
    )

    def clean_password(self):  # 钩取密码函数
        pwd = self.cleaned_data.get("password")  # 获取已输入的密码
        return md5(pwd)# 加密后与数据库验证

# 文章添加类
class ArticleAdd(BootsrapModel):
    tag = forms.ModelChoiceField(queryset= models.Choice.objects.all(), empty_label="请选择标签")
    class Meta:
        model = models.Article
        exclude = ["username", "status", "collect","tag","message","timemes"]

class ArticleEdit(BootsrapModel):
    select_tag = forms.ModelChoiceField(queryset= models.Choice.objects.all(),
                                        empty_label="请选择标签",
                                        label="请选择新标签：",
                                        blank=True,
                                        required=False)
    class Meta:
        model = models.Article
        exclude = ["username", "status", "collect"]
        widgets = {
            'tag': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


