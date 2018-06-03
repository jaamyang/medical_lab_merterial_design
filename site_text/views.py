#======================================================================
#
#        Copyright (C) 2018 medical_lab   
#        All rights reserved
#
#        filename :site_text views
#
#        created by soaki at 2018.5.20
#
#======================================================================

from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
from download import models as dlmod
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from . import models

EVERY_PAGE_LIST_NUM = 15
# Create your views here.

def page_list(type_str,list_num):
    type_object = get_object_or_404(models.Type,name = type_str)
    type_list = models.Text.objects.filter(text_type = type_object,invisible = False).order_by('-created_time')
    page_type = Paginator(type_list,int(list_num))
    return page_type

def get_text():
    cont = {}
    # type_news = get_object_or_404(models.Type,name = '新闻动态')
    # type_achievements = get_object_or_404(models.Type,name = '科研成果')
    # type_activity = get_object_or_404(models.Type,name = '学术活动')
    # type_notice = get_object_or_404(models.Type,name = '通知公告')
    # news = models.Text.objects.filter(text_type = type_news,is_delete = False).order_by('-created_time')
    # achievements = models.Text.objects.filter(text_type = type_activity,is_delete = False).order_by('-created_time')
    # activity = models.Text.objects.filter(text_type = achievements,is_delete = False).order_by('-created_time')
    # notice = models.Text.objects.filter(text_type = notice,is_delete = False).order_by('-created_time')
    page_news = page_list('新闻动态',EVERY_PAGE_LIST_NUM)
    page_achievements = page_list('科研成果',EVERY_PAGE_LIST_NUM)
    page_activity = page_list('学术活动',EVERY_PAGE_LIST_NUM)
    page_notice = page_list('通知公告',EVERY_PAGE_LIST_NUM)
    cont ['news'] = page_news.get_page(1)
    cont ['activity'] = page_activity.get_page(1)
    cont ['achievements'] = page_achievements.get_page(1)
    cont ['notice'] = page_notice.get_page(1)
    return cont

def get_text_to_index():
    context = {}
    context ['texts'] = models.Text.objects.filter(invisible = False).order_by('-created_time')[:5]
    return context


def information(request):
    context = {}
    context = get_text()
    return render(request,'information.html',context)

def text_detail(request,text_pk):
    context = {}
    text = get_object_or_404(models.Text,pk = text_pk)
    context['pervious_text'] = models.Text.objects.filter(created_time__lt = text.created_time,invisible = False).last()
    context['next_text'] = models.Text.objects.filter(created_time__gt = text.created_time,invisible = False).first()
    context ['text'] = text
    return render(request,'article.html',context) 

