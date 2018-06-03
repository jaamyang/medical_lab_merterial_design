from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.information,name = 'information'),
    path('<int:text_pk>/',views.text_detail,name = 'text_detail')
]