from django.urls import path
from . import views

urlpatterns = [
    path('teachers/', views.teacher.list, name='teacher-list'),
    path('teachers/<int:pk>/', views.teacher.detail, name='teacher-detail'),
    path('teachers/create/', views.teacher.create, name='teacher-create'),
    path('teachers/update/<int:pk>/', views.teacher.update, name='teacher-update'),
    path('teachers/delete/<int:pk>/', views.teacher.delete, name='teacher-delete'),
    path('teachers/search/<str:search>/', views.teacher.search, name='teacher-search'),
    path('students/', views.student.list, name='student-list'),
    path('students/<int:pk>/', views.student.detail, name='student-detail'),
    path('students/create/', views.student.create, name='student-create'),
    path('students/update/<int:pk>/', views.student.update, name='student-update'),
    path('students/delete/<int:pk>/', views.student.delete, name='student-delete'),
    path('students/search/<str:search>/', views.student.search, name='student-search'),
]
