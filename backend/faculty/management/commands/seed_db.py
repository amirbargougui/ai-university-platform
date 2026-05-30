from django.core.management.base import BaseCommand
from faculty.models import Department, Professor, Course, News
import random

class Command(BaseCommand):
    help = 'Remplit la base de données de la faculté'

    def handle(self, *args, **options):
        self.stdout.write('Nettoyage...')
        News.objects.all().delete()
        Course.objects.all().delete()
        Professor.objects.all().delete()
        Department.objects.all().delete()

        self.stdout.write('Création Départements...')
        d_info = Department.objects.create(name="Informatique", code="INFO", description="Études des systèmes informatiques, logiciels et réseaux.")
        d_math = Department.objects.create(name="Mathématiques", code="MATH", description="Sciences exactes, algèbre, analyse et statistiques.")
        d_law = Department.objects.create(name="Droit", code="LAW", description="Étude des lois, de la justice et des réglementations.")

        self.stdout.write('Création Professeurs...')
        p1 = Professor.objects.create(name="Dr. Alan Turing", title="Professeur", email="alan@uni.edu", department=d_info, bio="Pionnier de l'informatique théorique.", photo_url="https://picsum.photos/seed/turing/200/200")
        p2 = Professor.objects.create(name="Pr. Ada Lovelace", title="Maître de conférences", email="ada@uni.edu", department=d_info, bio="Première programmeuse de l'histoire.", photo_url="https://picsum.photos/seed/ada/200/200")
        p3 = Professor.objects.create(name="Dr. Carl Gauss", title="Professeur", email="gauss@uni.edu", department=d_math, bio="Le prince des mathématiciens.", photo_url="https://picsum.photos/seed/gauss/200/200")
        p4 = Professor.objects.create(name="Me. John Locke", title="Professeur", email="locke@uni.edu", department=d_law, bio="Philosophe et théoricien politique.", photo_url="https://picsum.photos/seed/locke/200/200")

        self.stdout.write('Création Cours...')
        Course.objects.create(code="INFO101", name="Introduction à la Programmation", credits=4, department=d_info, professor=p1, description="Bases de Python et algorithmique.")
        Course.objects.create(code="INFO202", name="Bases de Données", credits=3, department=d_info, professor=p2, description="SQL et conception de schémas.")
        Course.objects.create(code="MATH301", name="Algèbre Linéaire", credits=5, department=d_math, professor=p3, description="Vecteurs, matrices et espaces vectoriels.")
        Course.objects.create(code="LAW101", name="Droit Constitutionnel", credits=4, department=d_law, professor=p4, description="Fondements des institutions politiques.")

        self.stdout.write('Création Actualités...')
        News.objects.create(title="Rentrée Universitaire 2024", content="La rentrée est fixée au 15 septembre.", is_featured=True, image_url="https://picsum.photos/seed/campus/800/400")
        News.objects.create(title="Nouveau Laboratoire de Recherche", content="Le département INFO inaugure son nouveau labo IA.", is_featured=False, image_url="https://picsum.photos/seed/lab/800/400")
        News.objects.create(title="Conférence sur le Droit Numérique", content="Une conférence aura lieu vendredi prochain.", is_featured=False, image_url="https://picsum.photos/seed/conf/800/400")

        self.stdout.write(self.style.SUCCESS('Base de données peuplée avec succès !'))
