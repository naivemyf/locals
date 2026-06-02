from django.shortcuts import render
from django.db.models import Q
from app import models


def find(req):
    if req.method == 'GET':
        text = req.GET.get('search_text')
        a = req.GET.get('a')
        b = req.GET.get('b')
        content ={}
        if text:
            if b == None :
                list = models.Article.objects.filter(Q(title__contains=text) | Q(content__contains=text), status=2)
                content = {
                    "text": text,
                    "arts": list,
                }
            elif a == None:
                list = models.Commdity.objects.filter(Q(content__contains=text)| Q(commdityname__contains=text) ,status=1)
                content={
                    "text":text,
                    "comms":list,
                }
            return render(req, "user/find.html",content)
        return render(req, "user/find.html")