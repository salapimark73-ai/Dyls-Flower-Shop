from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='Inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create-account/', views.create_account, name='create-account'),
    path('profile/', views.profile, name='profile'),
    path('', views.index, name='home'),
    path('dashboard/', views.index, name='index'),
    path('flowers/new/', views.save_flower, name='flower-create'),
    path('flowers/<int:product_id>/edit/', views.save_flower, name='flower-edit'),
    path('flowers/<int:product_id>/delete/', views.delete_flower, name='flower-delete'),
]