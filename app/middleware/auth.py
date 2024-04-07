from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect

class AuthMiddleware(MiddlewareMixin):
    """登录中间件"""
    def process_request(self,req):
        #a.排除可直接访问的页面
        #当前请求的url:requset.path_info
        if req.path_info in ['','/index/','/login/','/image/code/','/register/','/article/list/']:
            return

        #b.读取当前用户的session信息
        info_dict = req.session.get("info")

        #判断是否存在
        if info_dict:
            return
        return redirect('/login/')
