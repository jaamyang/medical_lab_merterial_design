from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.download,name = 'download'),
    path('file/',views.file_download,name = 'file_download'),
    path('youwouldnotkonw/<int:file_pk>',views.download_util,name = 'whatthef'),
    # path('file/<int:file_pk>',views.test_download,name='test_file_download'),
    
]