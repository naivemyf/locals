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
from app.view import account, index, article, merchant, admin, commdity, localspec,test
from app.utils import uploadImage
from django.conf import settings
from django.conf.urls.static import static
# 新增页面，想要让未注册游客进入需要修改状态的中间件

urlpatterns = [


    #测试

    path("img/add/",test.add),  # 图片上传ceshi
    # # list模板
    # path("list/",list.list),
    #
    # 首页
    path("", index.index),  # 网站默认页面首页
    path("index/", index.index),  # 网站首页
    path('tag/<int:nid>/',index.tag),  # index标签页

    # 用户操作
    path("user/fav/",account.favindex),   # 用户收藏
    path("user/favcomm/",account.favindexcomm),   # 用户收藏
    path("user/<int:nid>/info/",account.myinfo),  # 用户信息
    path("user/myinfo/detail/",account.detail_myinfo),  # 用户信息详情
    path("user/myinfo/edit/",account.edit_myinfo),  # 用户信息编辑

    # 注册
    path("register/", account.register),  # 注册


    # 特产推荐算法
    # path("choice/sub/", localspec.choice_sub),  # 特产冷启动提交
    path("chocies/fav/",localspec.chocies),  # 特产选择


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
    path("admin/artlistno/admin/article/<int:nid>/view/",admin.art_detail),  # 文章详情
    path("admin/com/<int:nid>/view/",admin.comm_detail),  # 商品详情
    path("admin/comm/status/",admin.comm_status),   # 商品审核
    path("admin/comm/batch-audit/", admin.comm_batch),  # 文章批量审核
    path("admin/art/status/",admin.art_status),  # 文章审核
    path("admin/art/batch-audit/",admin.art_batch),  # 文章批量审核
    path("admin/art/nostatus/",admin.art_nostatus),  # 未通过审核
    path("admin/me/status/",admin.me_status),  # 商家审核
    path("admin/fav/",account.favindex),  # 管理员收藏
    path("admin/favcomm/",account.favindexcomm),  # 管理员收藏

    # 商家
    path("merchant/", merchant.merchantindex),  # 商家首页
    path("merchant/fav/", account.favindex),  # 商家收藏
    path("merchant/favcomm/", account.favindexcomm),  # 商家收藏

    # 商品
    path("commdity/add/", commdity.commdityadd),  # 商品添加
    path("commdity/list/", commdity.commditylistme),  # 我的商品列表
    path("commdity/listall/", commdity.commditylist),  # 全部商品列表
    path("commdity/<int:nid>/detail/", commdity.comm_detail),  # 商家商品详情
    path("commdity/<int:nid>/edit",commdity.comm_edit),  # 文章编辑
    path("commdity/delete/",commdity.comm_delete),  # 文章删除
    path("commdity/<int:id>/favorite/",commdity.comm_favorite),  # 商品收藏
    path("commdity/<int:id>/fav/del/",commdity.comm_fav_del),  # 商品取消收藏

    # 文章
    path("article/add/", article.articleadd),  # 文章添加
    path("uploadimage/",
         uploadImage.UploadImage.as_view(), name="upload_img"),  # 图片上传
    path("article/list/", article.list),  # 文章列表
    path("article/listme/",article.listme),  # 我的文章
    path("article/<int:nid>/detail/", article.art_detail),  # 文章详情
    path("article/<int:nid>/edit",article.art_edit),  # 文章编辑
    path("article/delete/",article.art_delete),  # 文章删除
    path("article/<int:id>/favorite/",article.art_favorite),  # 商品收藏
    path("article/<int:id>/fav/del/",article.art_fav_del),  # 商品取消收藏


]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
