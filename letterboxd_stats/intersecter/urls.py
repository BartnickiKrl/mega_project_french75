from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='intersect-home'),
    path('movie/',views.movie,name='intersect-movie')
]
