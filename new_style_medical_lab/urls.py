#======================================================================
#
#        Copyright (C) 2018 medical_lab   
#        All rights reserved
#
#        filename :homesite urls
#
#        created by soaki at 2018.5.20
#
#======================================================================

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name = 'home'),
    path('intro/',views.intro,name = 'intro'),
    path('information/',include('site_text.urls')),
    path('data_visual/',include('data_visual.urls')),
    path('download/',include('download.urls')),
    path('search/',views.search,name = 'search'),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('login/',views.login,name = 'login'),
    path('logout/',views.logout_view,name = 'logout'),
    path('search/',views.search,name = 'search'),
    # path('activities/',views.activities,name = 'activity'),
    # path('intro/',views.intro,name = 'intro'),
    # path('members/',views.members,name = 'members'),
    # path('achievements/',views.achievements,name = 'achievements'),
    # path('login/',views.login,name = 'login'),
    # path('detail/<int:text_pk>',views.text_detail,name = 'text_detail'),
    # path('ckeditor',include('ckeditor_uploader.urls')),
    # path('download/',include('download.urls')),
    # path('logout/',views.logout_view,name = 'logout'),
    # path('search/',views.search,name = 'search'),
    # path('data_visualization/',include('Data_visualization.urls')),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)