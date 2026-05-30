from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
# On n'importe pas 'User' depuis models pour éviter la confusion, on utilise get_user_model()
from .models import Professor, Course, Department, News
from .serializers import DepartmentSerializer, ProfessorSerializer, CourseSerializer, NewsSerializer
from rest_framework import viewsets

# --- DEFINITION DU MODELE UTILISATEUR ACTIF ---
User = get_user_model()

# --- FORMULAIRE PERSONNALISÉ ---
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')

# --- VUES WEB ---

def register(request):
    if request.method == 'POST':
        # IMPORTANT : Utiliser CustomUserCreationForm ici
        form = CustomUserCreationForm(request.POST)
        role = request.POST.get('role')
        
        if form.is_valid():
            user = form.save()
            
            # Attribution du rôle
            if role == 'professor':
                user.is_professor = True
            elif role == 'student':
                user.is_student = True
            
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})

@require_http_methods(["GET", "POST"])
def custom_login(request):
    """Vue de login personnalisée qui redirige toujours vers l'accueil (/)"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Toujours vers l'accueil, ignore le paramètre 'next'
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    
    if user.is_superuser:
        return render(request, 'dashboard_admin.html', {'user': user})
        
    elif user.is_professor:
        try:
            prof_profile = user.professor_profile
            my_courses = prof_profile.courses.all()
        except:
            my_courses = []
        return render(request, 'dashboard_prof.html', {'user': user, 'courses': my_courses})
        
    elif user.is_student:
    # Uniquement les cours où l'étudiant est inscrit
     enrolled_courses = Course.objects.filter(
        enrollments__student=user
    ).select_related('department', 'professor__user')
    return render(request, 'dashboard_student.html', {
        'user': user, 
        'courses': enrolled_courses
    })

# --- API ---

class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class ProfessorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Professor.objects.select_related('user', 'department').all()
    serializer_class = ProfessorSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.select_related('department', 'professor__user').all()
    serializer_class = CourseSerializer

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by('-date')
    serializer_class = NewsSerializer