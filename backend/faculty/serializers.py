from rest_framework import serializers
from .models import Department, Professor, Course, News, Enrollment

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description']

class ProfessorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Professor
        fields = ['id', 'name', 'email', 'title', 'bio', 'photo_url', 'department_name']

    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_email(self, obj):
        return obj.user.email

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'credits', 'description', 'department_name', 'professor_name']

    def get_professor_name(self, obj):
        if obj.professor:
            return f"{obj.professor.user.first_name} {obj.professor.user.last_name}"
        return "Non assigné"

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'date', 'image_url', 'is_featured']

class EnrollmentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name')
    course_code = serializers.CharField(source='course.code')
    credits = serializers.IntegerField(source='course.credits')
    professor_name = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = ['id', 'course_name', 'course_code', 'credits', 'professor_name', 'date_enrolled']

    def get_professor_name(self, obj):
        if obj.course.professor:
            return f"{obj.course.professor.user.first_name} {obj.course.professor.user.last_name}"
        return "Non assigné"