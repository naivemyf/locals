from django.http import JsonResponse
from django.conf import settings
from django.views.generic import View
# 引入屏蔽CSRF的方法
from django.views.decorators.csrf import csrf_exempt
# 类视图装饰器使用的时候，必须包裹在这个里面
from django.utils.decorators import method_decorator
class UploadImage(View):
    """富文本编辑器上传图片
    首先会检查项目根目录有没有media/upload/的文件夹
    如果没有就创建，图片最终保存在media/upload/目录下
    返回图片路径为 "/media/upload/file.png"
    如果因为权限不够，不能创建media，就手动进行创建。
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        import os
        import uuid
        file_data = request.FILES
        keys = list(file_data.keys())
        # 使用项目根目录拼接路径
        file_path = settings.BASE_DIR / 'app/static/pic/'
        if os.path.exists(file_path) is False:
            os.mkdir(file_path)
        # 返回数据中需要的data
        data = []
        for key in keys:
            img_dict = {}
            file = file_data.get(f'{key}')
            # 重命名文件名称
            names = list(os.path.splitext(file.name))
            names[0] = ''.join(str(uuid.uuid4()).split('-'))
            file.name = ''.join(names)
            new_path = os.path.join(file_path, file.name)
            # 开始上传
            with open(new_path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            # 构造返回数据
            img_dict['url'] = f"/app/static/pic/{file.name}"
            data.append(img_dict)
        context = {"errno": 0, "data": data}
        return JsonResponse(context)