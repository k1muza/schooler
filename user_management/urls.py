from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.teacher_list, name='teacher-list'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher-detail'),
    path('teachers/create/', views.teacher_create, name='teacher-create'),
    path('teachers/update/<int:pk>/', views.teacher_update, name='teacher-update'),
    path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher-delete'),
    path('teachers/search/<str:search>/', views.teacher_search, name='teacher-search'),
]
