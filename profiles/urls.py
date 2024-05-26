from django.urls import path
from . import views

urlpatterns = [
    path('user-profile/', views.user_profile, name='user_profile'),
    path('portfolios/', views.portfolio_list, name='portfolio_list'),
    path('portfolios/create/', views.portfolio_create, name='portfolio_create'),
    path('portfolios/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    path('portfolios/<int:portfolio_pk>/projects/create/', views.project_create, name='project_create'),
]