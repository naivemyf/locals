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
from app.view import account, index, article, merchant, admin, commdity
from app.utils import uploadImage
from django.conf import settings
from django.conf.urls.static import static
# 新增页面，想要让未注册游客进入需要修改状态的中间件

urlpatterns = [
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

    # 商家
    path("merchant/", merchant.merchantindex),  # 商家首页

    # 商品
    path("commdity/add/", commdity.commdityadd),  # 商品添加
    path("commdity/list/", commdity.commditylist),  # 商品列表

    # 文章

    path("article/add/", article.articleadd),  # 文章添加
    path("uploadimage/",
         uploadImage.UploadImage.as_view(), name="upload_img"),  # 图片上传
    path("article/list/", article.list),  # 文章列表
    path("article/listme/",article.listme),  # 我的文章

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
