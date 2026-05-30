from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle Utilisateur Personnalisé
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    def __str__(self): return f"{self.code} - {self.name}"

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    title = models.CharField(max_length=50) 
    department = models.ForeignKey(Department, related_name='professors', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self): return self.user.get_full_name() or self.user.username

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField(default=3)
    department = models.ForeignKey(Department, related_name='courses', on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, related_name='courses', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    def __str__(self): return f"{self.code}: {self.name}"

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    def __str__(self): return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    date_enrolled = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'course')  # un étudiant ne s'inscrit qu'une fois par cours
    
    def __str__(self):
        return f"{self.student.username} → {self.course.code}"

# ─────────────────────────────────────────────
# NOTES (NOUVEAU)
# ─────────────────────────────────────────────
class Grade(models.Model):
    EXAM_TYPES = [
        ('DS', 'Devoir Surveillé'),
        ('FINAL', 'Examen Final'),
        ('TP', 'Travaux Pratiques'),
        ('PROJET', 'Projet'),
        ('RATTRAPAGE', 'Rattrapage'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    value = models.FloatField()
    coefficient = models.FloatField(default=1.0)
    date = models.DateField()
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.username} | {self.course.code} | {self.exam_type} : {self.value}/20"


# ─────────────────────────────────────────────
# ABSENCES (NOUVEAU)
# ─────────────────────────────────────────────
class Absence(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='absences')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='absences')
    date = models.DateField()
    justified = models.BooleanField(default=False)
    reason = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        status = "justifiée" if self.justified else "non justifiée"
        return f"{self.student.username} | {self.course.code} | {self.date} ({status})"


# ─────────────────────────────────────────────
# PLANNING DES ÉPREUVES (NOUVEAU)
# ─────────────────────────────────────────────
class Exam(models.Model):
    EXAM_TYPES = [
        ('DS', 'Devoir Surveillé'),
        ('FINAL', 'Examen Final'),
        ('TP', 'Contrôle TP'),
        ('RATTRAPAGE', 'Rattrapage'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=120)
    room = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.course.code} | {self.exam_type} | {self.date.strftime('%d/%m/%Y %H:%M')}"