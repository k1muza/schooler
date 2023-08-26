from django.urls import path
from . import views

urlpatterns = [
    path('levels/', views.level_list, name='level-list'),
    path('levels/<int:pk>/', views.level_detail, name='level-detail'),
    path('levels/create/', views.level_create, name='level-create'),
    path('levels/update/<int:pk>/', views.level_update, name='level-update'),
    path('levels/delete/<int:pk>/', views.level_delete, name='level-delete'),
    path('levels/search/<str:search>/', views.level_search, name='level-search'),
]
