from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.data_visual_home,name = 'data_visual'),
    path('result',views.data_visual_process, name = 'result'),
    path('data_visual_upload/',views.upload_file,name = 'data_visual_upload'),
    path('data_process/',views.process_data,name = 'data_process'),
    
]