from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect

class AuthMiddleware(MiddlewareMixin):
    """登录中间件"""
    def process_request(self,req):
        #当前请求的url:requset.path_info
        # if req.path_info in ['','/index/','/login/','/image/code/','/register/','/article/list/',
        #                      '/chocies/fav/','/commdity/listall/','commdity/<int:nid>/detail/',
        #                      '/article/<int:nid>/detail/',]:
        #     return
        # info_dict = req.session.get("info")
        # if info_dict:
        #     return
        # return redirect('/login/')
        path =['/user/fav/', '/user/favcomm/','/logout/','/admin/','/merchant/','"/article/" + id + "/favorite/"']
        #  黑名单
        if req.path_info in path:
            info_dict = req.session.get("info")
            if not info_dict:
                return redirect('/login/')
            return
        return