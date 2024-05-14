import random
from collections import defaultdict
from django.db.models import Count
from app import models
from math import *
from collections import Counter

#  用户标签数据
def generate_user_enshrine_tag_count():
    # 用户标签数据
    # 时间复杂度是O(n*m)
    user_enshrine_tag_count = defaultdict(lambda: defaultdict(int))
    # 使用Python的collections模块中的defaultdict类创建的嵌套字典
    # 外层字典的默认值是一个内层字典，内层字典的默认值是整数0。
    # 这种数据结构可以方便地统计用户收藏的标签数量。
    enshrines = models.Enshrine.objects.filter(status=1)
    article_exists = {}
    commdity_exists = {}
    for enshrine in enshrines:
        user = enshrine.username
        tag = None
        if enshrine.art_id:
            for i in enshrine.art_id:
                if i not in article_exists:
                    article_exists[i] = models.Article.objects.filter(
                        id=i).exists()
                if article_exists[i]:
                    article = models.Article.objects.get(id=i)
                    tag = article.tag
        elif enshrine.comm_id:
            for i in enshrine.comm_id:
                if i not in commdity_exists:
                    commdity_exists[i] = models.Commdity.objects.filter(
                        id=i).exists()
                if commdity_exists[i]:
                    commdity = models.Commdity.objects.get(id=enshrine.comm_id)
                    tag = commdity.tag
        else:
            continue
        if tag:
            user_enshrine_tag_count[user][tag] += 1

    return user_enshrine_tag_count
    # 返回用户收藏的标签数量

#  计算用户之间的相似度
def Euclid(user1, user2, new_dicta):
    # 计算用户之间的相似度
    user1_data = new_dicta[user1]
    user2_data = new_dicta[user2]
    distance = 0
# 遍历第一个用户的所有键（评分项），
# 如果这个键也在第二个用户的键中，
# 计算这两个用户在这个评分项上的评分之差的平方,累加到总距离上。
    for key in user1_data.keys():
        if key in user2_data.keys():
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    # 距离开方，取其倒数，得到两个用户的相似度
    # 这个值越小，表示两个用户越相似
    return 1 / (1 + sqrt(distance))

#  构建最相似的用户top_people
def top_user(target_user, new_dicta):
    res = []
    for i in new_dicta.keys():
        if not i == target_user:
            simliar = Euclid(target_user, i, new_dicta)
            res.append((i, simliar))

    res.sort(key=lambda val: val[1])

    return res

#  构建推荐商品
def recommend(target_user, new_dicta):
    top_people = top_user(target_user, new_dicta)[0][0]
    recommed_list = {}
    # 获取当前相似度最高的用户的商品列表
    items = new_dicta[top_people]
    all_item = new_dicta[target_user]
    # 将两字典的值相加
    for key, value in items.items():
        if key in recommed_list:
            recommed_list[key] += value
        else:
            recommed_list[key] = value
    res_list = []
    for key, value in all_item.items():
        if key in recommed_list:
            recommed_list[key] += value
        else:
            recommed_list[key] = value
    count = models.Enshrine.objects.filter(username=target_user).count()
    if count > 5:
        res = most_list(target_user)
        res_list = res[0]
        # 将result转换为列表
        recommed_list = [(k, v) for k, v in recommed_list.items()]
        # 两个列表相加
        result_dict = {}
        for item in res_list:
            result_dict[item[0]] = item[1]
        for item in recommed_list:
            if item[0] in result_dict:
                result_dict[item[0]] += item[1]
            else:
                result_dict[item[0]] = item[1]
        result_list = [(k, v) for k, v in result_dict.items()]
        # 根据推荐列表里的打分请款从小到大排序，然后反转
        tuple = (result_list[:10], top_people)
    else:
        # 将result转换为列表
        recommed_list = [(k, v) for k, v in recommed_list.items()]
        tuple = (recommed_list[:10], top_people)
    # 取出top10推荐
    return tuple

#  收藏表里收藏最多的文章和商品，及标签(游客)
def top_recommed():
    """返回收藏表里收藏最多的文章和商品"""
    Enshrine = models.Enshrine.objects.all()
    most_enshrined_art = Enshrine.filter(art_id__isnull=False).values('art_id').annotate(
        count=Count('art_id')).order_by('-count')[:20].values_list('art_id', flat=True)
    most_enshrined_comm = Enshrine.filter(comm_id__isnull=False).values('comm_id').annotate(
        count=Count('comm_id')).order_by('-count')[:20].values_list('comm_id', flat=True)

    most_enshrined_tags = []
    # 根据ID列表查询对应的tag
    for art_id in most_enshrined_art:
        most_enshrined_tags.extend(
            models.Article.objects.filter(
                id=art_id).values_list(
                'tag',
                flat=True))
    for comm_id in most_enshrined_comm:
        exists = models.Commdity.objects.filter(id=comm_id).exists()
        if not exists:
            continue
        most_enshrined_tags.extend(
            models.Commdity.objects.filter(
                id=comm_id).values_list(
                'tag',
                flat=True))

    # 统计每个tag的收藏次数
    tag_counts = {}
    for tag in most_enshrined_tags:
        if not tag:
            continue
        if tag in tag_counts:
            tag_counts[tag] += 1
        else:
            tag_counts[tag] = 1
    # 按收藏次数降序排列，取前10个
    top_tags = sorted(
        tag_counts.items(),
        key=lambda x: x[1],
        reverse=True)[
        :20]
    top_tuple = (most_enshrined_art, most_enshrined_comm, top_tags)
    return top_tuple

def most_list(name):
    enshrines = models.Enshrine.objects.filter(username=name)  # 查找用户的收藏记录
    tag = []
    for enshrine in enshrines:
        if enshrine.art_id:
            try:
                art = models.Article.objects.get(id=enshrine.art_id)
                tag_art = art.tag
                tag.append(tag_art)
            except models.Article.DoesNotExist:
                pass
        if enshrine.comm_id:
            try:
                comm = models.Commdity.objects.get(id=enshrine.comm_id)
                tag_comm = comm.tag
                tag.append(tag_comm)
            except models.Commdity.DoesNotExist:
                pass
    counter = Counter(tag)
    res = list(counter.items())
    new_res = [item for item in res if item[0] is not None]
    most_list = (new_res, res)
    return most_list

# 随机推荐文章和商品
def random_list():
    mess_art=[]
    mess_comm =[]
    art_exists = models.Article.objects.filter(status=2).exists()
    if art_exists:
        art_ids = models.Article.objects.filter(status=2).values_list("id",flat=True)
        art_ids = list(art_ids)
        random.shuffle(art_ids)
        mess_art = art_ids[:20]
    comm_exists = models.Commdity.objects.filter(status=1).exists()
    if comm_exists:
        comm_ids = models.Commdity.objects.filter(status=1).values_list("id", flat=True)
        comm_ids = list(comm_ids)
        random.shuffle(comm_ids)
        mess_comm = comm_ids[:20]
    mess = {
        "art_ids": mess_art,
        "comm_ids": mess_comm,
    }
    return mess