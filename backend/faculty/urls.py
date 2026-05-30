from django.urls import path, include
from rest_framework.routers import DefaultRouter
from faculty.views import DepartmentViewSet, ProfessorViewSet, CourseViewSet, NewsViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'professors', ProfessorViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls))
]