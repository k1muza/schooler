from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'students', views.student.StudentViewSet, basename='student')
router.register(r'teachers', views.teacher.TeacherViewSet, basename='teacher')

urlpatterns = [
    path('', include(router.urls))
]
