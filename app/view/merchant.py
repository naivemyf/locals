from django.shortcuts import render,redirect

from app import models


def merchantindex(req):
    cname= req.session["info"]["name"]
    comm_counts = models.Commdity.objects.filter(username=cname).count()
    ad_comm = models.Commdity.objects.filter(username=cname, status=1).count()
    unad_comm = models.Commdity.objects.filter(username=cname, status=0).count()
    data ={
        "comm_counts": comm_counts,
        "ad_comm": ad_comm,
        "unad_comm": unad_comm
    }
    return render(req, 'merchant/merchant.html',{"data": data})

