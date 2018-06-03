from django.views.decorators.http import require_POST
from django.shortcuts import render,get_object_or_404,redirect
from django.http import FileResponse,JsonResponse,HttpResponse
from django.contrib.auth.models import User,Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from . import models

# Create your views here.

def list_in(list1,list2):
        if list1:
            for e in list1:
                if e in list2:
                    return True
            return False
        else:
            return False

def getPages(request,objectlist):
    """get the paginator"""
    currentPage = request.GET.get('page', 1)
    paginator = Paginator(objectlist,5)
    objectlist = paginator.page(currentPage)
 
    page_range = []
    current = objectlist.number     #当前页码
    page_all = paginator.num_pages  #总页数
    mid_pages = 3                   #中间段显示的页码数
    page_goto = 1                   #默认跳转的页码
 
    #获取优化显示的页码列表
    if page_all <= 2 + mid_pages:
        #页码数少于6页就无需分析哪些地方需要隐藏
        page_range = paginator.page_range
    else:
        #添加应该显示的页码
        page_range += [1, page_all]
        page_range += [current-1, current, current+1]
 
        #若当前页是头尾，范围拓展多1页
        if current == 1 or current == page_all:
            page_range += [current+2, current-2]
 
        #去掉超出范围的页码
        page_range = filter(lambda x: x>=1 and x<=page_all, page_range)
 
        #排序去重
        page_range = sorted(list(set(page_range)))
 
        #查漏补缺
        #从第2个开始遍历，查看页码间隔，若间隔为0则是连续的
        #若间隔为1则补上页码；间隔超过1，则补上省略号
        t = 1
        for i in range(len(page_range)-1):
            step = page_range[t]-page_range[t-1]
            if step>=2:
                if step==2:
                    page_range.insert(t,page_range[t]-1)
                else:
                    page_goto = page_range[t-1] + 1
                    page_range.insert(t,'...')
                t+=1
            t+=1
 
    #优化结果之后的页码列表
    paginator.page_range_ex = page_range
    #默认跳转页的值
    paginator.page_goto = page_goto
 
    return paginator,objectlist


def download(request):
    context = {}    
    files = models.Download_file.objects.filter(invisible = False).order_by('-upload_date')
    pages = Paginator(files, 10) 
    current_page = request.GET.get("page",1)
    print(current_page,pages.page_range)
    context['files'] =  pages.get_page(current_page)
    context['page'] = pages #pages.get_page(current_page)
    return render(request,'download.html',context)

def download_util(request,file_pk):
    download_file = get_object_or_404(models.Download_file,pk = file_pk)
    file=open(download_file.file.path,'rb') 
    response =FileResponse(file)  
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename='+"".join(download_file.file.name.split('/')[-1:]).encode('utf-8').decode('ISO-8859-1')
    return response  

@require_POST
def file_download(request):
    file_pk = request.POST["file_pk"]
    download_file = get_object_or_404(models.Download_file,pk = file_pk)

    user_group = []
    file_group = []
    if request.user.is_authenticated:
        for e in get_object_or_404(User,username = request.user).groups.all():
            user_group.append(e.name)    
    for e in download_file.download_permission.all():
        file_group.append(e.name)

    #print(user_group,file_group)
    if '任何人' in file_group or list_in(user_group,file_group):         
        return HttpResponse(reverse('whatthef', args=[file_pk]))    
    else:
        return HttpResponse('true')