from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'students', views.student.StudentViewSet, basename='student')

urlpatterns = [
    path('teachers/', views.teacher.list, name='teacher-list'),
    path('teachers/<int:pk>/', views.teacher.detail, name='teacher-detail'),
    path('teachers/create/', views.teacher.create, name='teacher-create'),
    path('teachers/update/<int:pk>/', views.teacher.update, name='teacher-update'),
    path('teachers/delete/<int:pk>/', views.teacher.delete, name='teacher-delete'),
    path('teachers/search/<str:search>/', views.teacher.search, name='teacher-search'),
    path('', include(router.urls))
]
