from django.urls import path
from . import views

urlpatterns = [
    # Define your subdomain-specific URL patterns here
    path('', views.index, name='index'),
    path('update/', views.upload_file, name='upload_file'),
    path('price_list/', views.price_list, name='price_list'),
    path('query_list/', views.query_results, name='query_results'),
    path('success/', views.success, name='success'),
]
