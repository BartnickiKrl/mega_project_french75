from django.urls import path

from . import views

urlpatterns = [
    path('',views.intersect,name='intersect-home')
]
