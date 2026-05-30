from django.contrib import admin
from .models import Department, Professor, Course, News

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'title', 'department')
    list_filter = ['department']

    # Cette fonction permet d'afficher le nom de l'utilisateur lié
    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = 'Nom du Professeur'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits', 'department', 'professor']
    list_filter = ['department']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'is_featured']
    list_filter = ['is_featured']