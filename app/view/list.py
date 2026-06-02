from django.shortcuts import render


def list(req):
    return render(req, "AllcommdityList.html")