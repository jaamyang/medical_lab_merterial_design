#======================================================================
#
#        Copyright (C) 2018 medical_lab   
#        All rights reserved
#
#        filename :homesite view 
#
#        created by soaki at 2018.5.20
#
#======================================================================

from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from site_text import models as text_model
from site_text import views as text_views
from download import models as dlmod


def home(request):
    context  = text_views.get_text_to_index()
    return render(request,'home.html',context)

def intro(request):
    context = {}
    context['intro'] = text_model.Text.objects.filter(text_type = get_object_or_404(text_model.Type,name = 'intro'))[0]
    return render(request,'intro.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            #raise forms.ValidationError(u"两次密码必须一致")
            #return render(request,'error.html',{'message':'用户名或密码错误!'})
            return render(request,'login.html',{'error_message':'true'})
    else:
        return render(request,'login.html')

def logout_view(request):
    auth.logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def search(request):
    search_key = request.GET.get('search_key')
    print(search_key == '')
    if search_key == '':
        return render(request,'404.html')
    search_condition = request.GET.get('condition','title')
    print(search_key,search_condition)
    print(search_condition=='title')
    text_results = []
    file_results = []
    if search_condition =='title':
        text_results = text_model.Text.objects.filter(title__icontains = search_key,invisible = False)
    elif search_condition == 'author':
        author = get_object_or_404(User,username = search_key)
        text_results = text_model.Text.objects.filter(author = author,invisible = False)
    elif search_condition == 'content':
        text_results = text_model.Text.objects.filter(content__icontains = search_key,invisible = False)
    else:
        file_results = dlmod.Download_file.objects.filter(file_name__icontains = search_key)
    return render(request, 'search.html', {'text_results': text_results,'file_results':file_results})