"""
URL configuration for Localspecialty project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.view import account, index, article, merchant, admin, commdity,list
from app.utils import uploadImage
from django.conf import settings
from django.conf.urls.static import static
# 新增页面，想要让未注册游客进入需要修改状态的中间件

urlpatterns = [
    # list模板
    path("list/",list.list),

    # 首页
    path("", index.index),  # 网站默认页面首页
    path("index/", index.index),  # 网站首页

    # 注册
    path("register/", account.register),  # 注册

    # 登录
    path("login/", account.login),  # 登录
    path("logout/", account.logout),  # 注销
    path("image/code/", account.image_code),  # 验证码

    # 管理员
    path("admin/", admin.adminindex),  # 管理员首页
    path("admin/artlist/",admin.ad_art_list),  # 已审核文章列表
    path("admin/artlistno/",admin.ad_art_list_no),  # 管理员未审核文章列表
    path("admin/melist/",admin.ad_me_list),  # 已审核商家
    path("admin/melistno/",admin.ad_me_listno),  # 未审核商家
    path("admin/commlist/",admin.ad_comm_list),  # 已审核商品
    path("admin/commlistno/",admin.ad_comm_listno),  # 已审核商品



    # 商家
    path("merchant/", merchant.merchantindex),  # 商家首页

    # 商品
    path("commdity/add/", commdity.commdityadd),  # 商品添加
    path("commdity/list/", commdity.commditylistme),  # 我的商品列表
    path("commdity/listall/", commdity.commditylist),  # 全部商品列表
    # path("commdity/pic/", commdity.commdityPic),  # 商品图片
    path("commdity/<int:nid>/detail/", commdity.comm_detail),  # 商家商品详情
    path("commdity/all/<int:nid>/detail/",commdity.comm_all_detail),  # 用户页面商品详情
    path("commdity/<int:nid>/edit",commdity.comm_edit),  # 文章编辑
    path("commdity/delete/",commdity.comm_delete),  # 文章删除

    # 文章
    path("article/add/", article.articleadd),  # 文章添加
    path("uploadimage/",
         uploadImage.UploadImage.as_view(), name="upload_img"),  # 图片上传
    path("article/list/", article.list),  # 文章列表
    path("article/listme/",article.listme),  # 我的文章
    path("article/<int:nid>/detail/", article.art_detail),  # 文章详情
    path("article/<int:nid>/edit",article.art_edit),  # 文章编辑
    path("article/delete/",article.art_delete),  # 文章删除


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
