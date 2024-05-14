#
from django.utils.safestring import mark_safe

# 文章
class Pagination(object):
    # 视图函数中
    # def list(req):
    #   选择数据(xxx数据表)
    #   queryset = models.xxx.objects.all()
    #   实例化对象
    #   page_object =Pagination(req,queryset)
    #
    #   context={
    #       "queryset":page_object.page_queryset
    #        "page_string":page_object.html()
    #   }
    #   return render(req,'xxxx.htm',context)
    #
    # 在HTML中
    # < ul class ="pagination" >
    #   {{page_string}}
    # </ul>

    # 初始化
    def __init__(
            self,
            requset,
            queryset,
            page_size=20,
            page_param="page",
            plus=5):
        """
        :param requset: 请求对象
        :param queryset: 数据表
        :param page_size: 每页的数据条数
        :param page_param: 在url中传递的页码例如;?page=xx
        :param plus: 当前页的前或者后几页的页码
        """
        page = requset.GET.get(page_param, 1)
        page =str(page)
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            if self.page <= self.plus:
                # 小于5页
                start_page = 1
                end_page = 2 * self.plus + 2
            else:
                if self.page + self.plus >= self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self. page + self. plus + 1

        # start_page = page - plus
        # end_page = page + plus + 1

        # 页码
        page_str_list = []
        # 首页
        prev = '<li > <a href = "?page={}"> 首页</a> </li>'.format(1)
        page_str_list.append(prev)
        # 上一页
        if self.page > 1:
            prev = '<li > <a href = "?page={}"> 上一页</a> </li>'.format(
                self.page - 1)
        else:
            prev = '<li > <a href = "?page={}"> 上一页</a> </li>'.format(1)
        page_str_list.append(prev)
        # 中间页
        for i in range(start_page, end_page):
            if i == self.page:
                ele = '<li class="active"> <a href = "?page={}"> {}</a> </li>'.format(
                    i, i)
            else:
                ele = '<li> <a href = "?page={}"> {}</a> </li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            prev = '<li > <a href = "?page={}"> 下一页</a> </li>'.format(
                self.page + 1)
        else:
            prev = '<li > <a href = "?page={}"> 下一页</a> </li>'.format(
                self.total_page_count)
        page_str_list.append(prev)
        # 尾页
        prev = '<li > <a href = "?page={}"> 尾页</a> </li>'.format(
            self.total_page_count)
        page_str_list.append(prev)
        page_string = mark_safe("".join(page_str_list))
        return page_string

# 商品
class PaginationComm(object):
    # 视图函数中
    # def list(req):
    #   选择数据(xxx数据表)
    #   queryset = models.xxx.objects.all()
    #   实例化对象
    #   page_object =Pagination(req,queryset)
    #
    #   context={
    #       "queryset":page_object.page_queryset
    #        "page_string":page_object.html()
    #   }
    #   return render(req,'xxxx.htm',context)
    #
    # 在HTML中
    # < ul class ="pagination" >
    #   {{page_string}}
    # </ul>

    # 初始化
    def __init__(
            self,
            requset,
            queryset,
            page_size=15,
            page_param="page",
            plus=5):
        """
        :param requset: 请求对象
        :param queryset: 数据表
        :param page_size: 每页的数据条数
        :param page_param: 在url中传递的页码例如;?page=xx
        :param plus: 当前页的前或者后几页的页码
        """
        page = requset.GET.get(page_param, 1)
        page =str(page)
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            if self.page <= self.plus:
                # 小于5页
                start_page = 1
                end_page = 2 * self.plus + 2
            else:
                if self.page + self.plus >= self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self. page + self. plus + 1

        # start_page = page - plus
        # end_page = page + plus + 1

        # 页码
        page_str_list = []
        # 首页
        prev = '<li > <a href = "?page={}"> 首页</a> </li>'.format(1)
        page_str_list.append(prev)
        # 上一页
        if self.page > 1:
            prev = '<li > <a href = "?page={}"> 上一页</a> </li>'.format(
                self.page - 1)
        else:
            prev = '<li > <a href = "?page={}"> 上一页</a> </li>'.format(1)
        page_str_list.append(prev)
        # 中间页
        for i in range(start_page, end_page):
            if i == self.page:
                ele = '<li class="active"> <a href = "?page={}"> {}</a> </li>'.format(
                    i, i)
            else:
                ele = '<li> <a href = "?page={}"> {}</a> </li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            prev = '<li > <a href = "?page={}"> 下一页</a> </li>'.format(
                self.page + 1)
        else:
            prev = '<li > <a href = "?page={}"> 下一页</a> </li>'.format(
                self.total_page_count)
        page_str_list.append(prev)
        # 尾页
        prev = '<li > <a href = "?page={}"> 尾页</a> </li>'.format(
            self.total_page_count)
        page_str_list.append(prev)
        page_string = mark_safe("".join(page_str_list))
        return page_string