from django.urls import path
from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('search', views.search_form, name='search_form'),
    path('image', views.image_form, name='image_form'),
]
