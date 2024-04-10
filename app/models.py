from django.db import models

#数据库创建
# Create your models here.
class Role(models.Model):
    """ 角色表"""
    rolename = models.CharField(verbose_name='角色名',max_length=16)
    #0:用户，1：商家，2管理员

    def __str__(self):
        return self.rolename

class User(models.Model):
    """用户表"""
    username = models.CharField(verbose_name='姓名',max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    phonenumber = models.CharField(verbose_name="手机号",max_length=11)
    createtime = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    #auto_now_add=True创建时间自动生成
    role = models.ForeignKey(to="Role",to_field="id",on_delete=models.CASCADE,verbose_name="角色名")
    #1: 用户，2：商家，3管理员
    #to="Role"关联角色表
    #to_fields="id"关联角色表的id
    #on_delete=models.CASCADE删除时级联删除
    # #deafult=0默认为0
    subadmin_choices = (
        (0,"普通使用者"),
        (1,"申请子管理员"),
        (2, "子管理员"),
        (3, "系统管理员"))
    subadmin = models.SmallIntegerField(verbose_name="管理员类别",choices=subadmin_choices,default=0)

    process_choices =(
        (0, "待审核"),
        (1, "审核通过")
    )
    process = models.SmallIntegerField(verbose_name="审核状态",choices=process_choices,default=1)
    def __str__(self):#用str函数使modelform中可自动生成user中的内容
        return self.username #返回用户名


class Area(models.Model):
    area_name = models.CharField(verbose_name="地区名", max_length=16)
    def __str__(self):
        return self.area_name


class Commdity(models.Model):
    """商品表"""
    commdityname = models.CharField(verbose_name="商品名", max_length=24)
    price = models.IntegerField(verbose_name="价格")
    createtime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    form = models.CharField(verbose_name="成份", max_length=128)
    area = models.ForeignKey(to="Area", to_field="id", verbose_name="地区", on_delete=models.CASCADE)
    status_choice = (
        (0, "待审核"),
        (1, "审核通过")
    )
    pic = models.ImageField(upload_to="users",blank=True, null=True, verbose_name='商品图片')
    status = models.SmallIntegerField(verbose_name="审核状态", choices=status_choice, default=0)
    username = models.CharField(verbose_name="商家", max_length=16,null=True)
    def __str__(self):
        return self.commdityname

class Article(models.Model):
    """文章表"""
    title = models.CharField(verbose_name='标题',max_length=16)
    timestamp = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    username = models.ForeignKey(to="User",to_field="id",verbose_name="作者",on_delete=models.CASCADE)
    content = models.TextField(verbose_name="内容")
    commdity = models.ForeignKey(to="Commdity",to_field="id",verbose_name="商品",on_delete=models.CASCADE, null=True,blank=True)
    status_choice =(
        (0, "待审核"),
        (1, "审核通过")
    )
    status = models.SmallIntegerField(verbose_name="审核状态", choices=status_choice, default=0)
    collect_choice =(
        (0, "否"),
        (1, "是")
    )
    collect = models.SmallIntegerField(verbose_name="是否收藏",choices=collect_choice,default=0)


class Enshrine(models.Model):
    """收藏表"""
    article = models.ForeignKey(to="Article",to_field="id",on_delete=models.CASCADE,verbose_name="文章id")
    commdity= models.ForeignKey(to="Commdity", to_field="id", on_delete=models.CASCADE, verbose_name="商品id")
    enshrinetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
