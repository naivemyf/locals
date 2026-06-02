from django.utils.safestring import mark_safe


class Pagination(object):
    """
    通用分页组件

    视图函数中使用:
        def list(req):
            queryset = models.SomeModel.objects.all()
            page_obj = Pagination(req, queryset)
            context = {
                "queryset": page_obj.page_queryset,
                "page_string": page_obj.html(),
            }
            return render(req, 'xxx.html', context)

    HTML 中使用:
        <ul class="pagination">
            {{ page_string }}
        </ul>
    """

    def __init__(self, requset, queryset, page_size=20, page_param="page", plus=5):
        """
        :param requset: 请求对象
        :param queryset: 数据表
        :param page_size: 每页的数据条数
        :param page_param: URL 中传递的页码参数，例如 ?page=xx
        :param plus: 当前页前/后各显示几页的页码
        """
        page = requset.GET.get(page_param, 1)
        page = str(page)
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
                start_page = 1
                end_page = 2 * self.plus + 2
            else:
                if self.page + self.plus >= self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1

        page_str_list = []

        # 首页
        page_str_list.append(
            '<li><a href="?page={}">首页</a></li>'.format(1)
        )

        # 上一页
        prev_page = max(self.page - 1, 1)
        page_str_list.append(
            '<li><a href="?page={}">上一页</a></li>'.format(prev_page)
        )

        # 中间页
        for i in range(start_page, end_page):
            if i == self.page:
                ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
            else:
                ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
            page_str_list.append(ele)

        # 下一页
        next_page = min(self.page + 1, self.total_page_count)
        page_str_list.append(
            '<li><a href="?page={}">下一页</a></li>'.format(next_page)
        )

        # 尾页
        page_str_list.append(
            '<li><a href="?page={}">尾页</a></li>'.format(self.total_page_count)
        )

        return mark_safe("".join(page_str_list))


class PaginationComm(Pagination):
    """商品分页组件 —— 继承 Pagination，仅默认每页数量不同"""

    def __init__(self, requset, queryset, page_size=15, page_param="page", plus=5):
        super().__init__(requset, queryset,
                         page_size=page_size, page_param=page_param, plus=plus)
