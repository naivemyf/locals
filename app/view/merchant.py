from django.shortcuts import render,redirect

def merchantindex(req):
    return render(req, 'merchant.html')