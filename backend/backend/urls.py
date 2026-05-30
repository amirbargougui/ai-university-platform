'''from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from faculty.views import register, dashboard

urlpatterns = [
    # 1. Administration (PhpMyAdmin-like)
    path('admin/', admin.site.urls),
    
    # 2. Authentification
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # 3. Tableaux de bord
    path('dashboard/', dashboard, name='dashboard'),

    #6. url agent 
    path('api/agent/', include('agent.urls')), 
    
    # 4. API REST (Pour le site public)
    # Ici on inclut 'faculty.urls', PAS 'backend.urls' !
    path('api/', include('faculty.urls')),
    
    # 5. Page d'accueil publique
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
      



]'''
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from faculty.views import register, custom_login, dashboard

urlpatterns = [
    # 1. Administration
    path('admin/', admin.site.urls),

    # 2. Authentification
    path('register/', register, name='register'),
    path('login/', custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # 3. Tableaux de bord
    path('dashboard/', dashboard, name='dashboard'),

    # 4. Agent IA (AVANT api/ pour éviter le conflit)
    path('api/agent/', include('agent.urls')),

    # 5. API REST faculty
    path('api/', include('faculty.urls')),

    # 6. Pages publiques
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('apropos/', TemplateView.as_view(template_name='apropos.html'), name='apropos'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('departements/', TemplateView.as_view(template_name='departements.html'), name='departements'),
]
