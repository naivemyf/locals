# Create your models here.

from django.db import models
from ckeditor.fields import RichTextField

from ckeditor_uploader.fields import RichTextUploadingField
# 数据库创建
# Create your models here.


class Role(models.Model):
    """ 角色表"""
    rolename = models.CharField(verbose_name='角色名', max_length=16)
    # 0:用户，1：商家，2管理员

    def __str__(self):
        return self.rolename


class User(models.Model):
    """用户表"""
    username = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    phonenumber = models.CharField(verbose_name="手机号", max_length=11)
    createtime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    # auto_now_add=True创建时间自动生成
    role = models.ForeignKey(
        to="Role",
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name="角色名")
    # 1: 用户，2：商家，3管理员
    # to="Role"关联角色表
    # to_fields="id"关联角色表的id
    # on_delete=models.CASCADE删除时级联删除
    # #deafult=0默认为0
    subadmin_choices = (
        (0, "普通使用者"),
        (1, "申请子管理员"),
        (2, "子管理员"),
        (3, "系统管理员"))
    subadmin = models.SmallIntegerField(
        verbose_name="管理员类别",
        choices=subadmin_choices,
        default=0)

    process_choices = (
        (0, "待审核"),
        (1, "审核通过")
    )  # 商家审核字段
    process = models.SmallIntegerField(
        verbose_name="审核状态",
        choices=process_choices,
        default=1)

    def __str__(self):  # 用str函数使modelform中可自动生成user中的内容
        return self.username  # 返回用户名


class Commdity(models.Model):
    """商品表"""
    commdityname = models.CharField(verbose_name="特产名", max_length=24)

    createtime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    form = models.CharField(verbose_name="成份", max_length=128)
    content = models.TextField(verbose_name="描述", blank=True, null=True)
    # food = models.ForeignKey(to="Food", to_field="id", verbose_name="特产分类", on_delete=models.CASCADE,blank=True,null=True)
    status_choice = (
        (0, "待审核"),
        (1, "审核通过")
    )
    pic = models.ImageField(
        upload_to="users",
        blank=True,
        null=True,
        verbose_name='特产图片')
    status = models.SmallIntegerField(
        verbose_name="审核状态",
        choices=status_choice,
        default=0)
    username = models.CharField(verbose_name="商家", max_length=16, null=True)
    tag = models.CharField(
        verbose_name="标签",
        blank=True,
        null=True,
        max_length=32)
    message = models.CharField(max_length=512, verbose_name="备注", null=True, blank=True)
    timemes = models.DateTimeField(verbose_name="信息时间",null=True, blank=True)

    def __str__(self):
        return self.commdityname


class Article(models.Model):
    """文章表"""
    title = models.CharField(verbose_name='标题', max_length=128)
    timestamp = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    username = models.CharField(verbose_name="作者", max_length=16, null=True)
    content = models.TextField(verbose_name="内容")
    commdity = models.ForeignKey(
        to="Commdity",
        to_field="id",
        verbose_name="特产",
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    tag = models.CharField(
        verbose_name="标签",
        blank=True,
        null=True,
        max_length=32)
    status_choice = (
        (0, "待审核"),
        (1, "初步审核"),
        (2, "审核通过")
    )
    status = models.SmallIntegerField(
        verbose_name="审核状态",
        choices=status_choice,
        default=0)
    message = models.CharField(max_length=512,verbose_name="备注",null=True,blank=True)
    timemes = models.DateTimeField(verbose_name="信息时间", null=True, blank=True)


class Enshrine(models.Model):
    """收藏表"""
    username = models.CharField(verbose_name='用户名', max_length=16)
    art_id = models.CharField(
        verbose_name='文章id',
        max_length=16,
        null=True,
        blank=True)
    comm_id = models.CharField(
        verbose_name='商品id',
        max_length=16,
        null=True,
        blank=True)
    enshrinetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    status_choice = (
        (0, "无效"),
        (1, "有效"),
    )
    status = models.SmallIntegerField(
        verbose_name="状态", choices=status_choice, default=1)

class Choice(models.Model):
    """选择兴趣表"""
    name = models.CharField(verbose_name='特产分类名称', max_length=16)
    pic = models.ImageField(
        upload_to="localblank",
        blank=True,
        null=True,
        verbose_name='特产分类图片')

    def __str__(self):
        return self.name

class Recommend(models.Model):

    user = models.CharField(verbose_name='用户名', max_length=16)
    score = models.CharField(
        verbose_name='评分',
        max_length=64,
        blank=True,
        null=True,
    )

class Merchant(models.Model):
    company_name = models.CharField(max_length=255, verbose_name='公司名称')
    company_chice = (
        (0, "有限责任公司 "),
        (1, "股份有限公司" ),
        (2, "无限公司"),
        (3, "两合公司"),
        (4, "股份两合公司"),
    )
    company_type = models.SmallIntegerField(verbose_name='公司类型',choices =company_chice)

    representative_name = models.CharField(max_length=255, verbose_name='法定代表人姓名')
    id_number = models.CharField(max_length=18, verbose_name='法人身份证号码')
    id_expiration_date = models.DateField(verbose_name='法人身份证有效期')
    contact_phone = models.CharField(max_length=20, verbose_name='联系电话')
    actual_office_address = models.CharField(max_length=255, verbose_name='实际办公地址')
    password = models.CharField(max_length=255, verbose_name='密码')

    def __str__(self):
        return self.company_name


class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    name = models.CharField(max_length=255, verbose_name='发送者')