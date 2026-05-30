"""
Script de chargement des données fictives - Faculté d'Informatique
Exécuter avec : python manage.py shell < seed_data.py
Ou copier-coller dans le shell Django
"""

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from faculty.models import User, Department, Professor, Course, News, Enrollment, Grade, Absence, Exam

print("Nettoyage des données existantes...")
Exam.objects.all().delete()
Absence.objects.all().delete()
Grade.objects.all().delete()
Enrollment.objects.all().delete()
News.objects.all().delete()
Course.objects.all().delete()
Professor.objects.all().delete()
Department.objects.all().delete()
User.objects.filter(is_superuser=False).delete()

print("Création des départements...")
dept_info = Department.objects.create(
    name="Département Informatique",
    code="INFO",
    description="Formation en génie logiciel, algorithmes, réseaux et systèmes d'information."
)
dept_math = Department.objects.create(
    name="Département Mathématiques & Informatique",
    code="MINFO",
    description="Formation hybride alliant fondements mathématiques et informatique appliquée."
)
dept_reseau = Department.objects.create(
    name="Département Réseaux & Télécommunications",
    code="RT",
    description="Formation en infrastructures réseau, sécurité et protocoles de communication."
)
dept_si = Department.objects.create(
    name="Département Systèmes d'Information",
    code="SI",
    description="Formation en conception, développement et gestion des systèmes d'information."
)

print("Création des utilisateurs professeurs...")
prof_users = [
    {"username": "benali.karim",   "first_name": "Karim",   "last_name": "Benali",   "email": "k.benali@faculte-info.dz"},
    {"username": "hamdi.sara",     "first_name": "Sara",    "last_name": "Hamdi",    "email": "s.hamdi@faculte-info.dz"},
    {"username": "khelifi.omar",   "first_name": "Omar",    "last_name": "Khelifi",  "email": "o.khelifi@faculte-info.dz"},
    {"username": "messaoud.lina",  "first_name": "Lina",    "last_name": "Messaoud", "email": "l.messaoud@faculte-info.dz"},
    {"username": "boudiaf.tarek",  "first_name": "Tarek",   "last_name": "Boudiaf",  "email": "t.boudiaf@faculte-info.dz"},
    {"username": "ferhat.nadia",   "first_name": "Nadia",   "last_name": "Ferhat",   "email": "n.ferhat@faculte-info.dz"},
    {"username": "aissa.youcef",   "first_name": "Youcef",  "last_name": "Aissa",    "email": "y.aissa@faculte-info.dz"},
    {"username": "ziani.malika",   "first_name": "Malika",  "last_name": "Ziani",    "email": "m.ziani@faculte-info.dz"},
]

created_prof_users = []
for u in prof_users:
    user = User.objects.create_user(
        username=u["username"],
        first_name=u["first_name"],
        last_name=u["last_name"],
        email=u["email"],
        password="prof@2024",
        is_professor=True,
        is_staff=False,
        is_active=True,
    )
    created_prof_users.append(user)

print("Création des profils professeurs...")
professors = [
    {"user": created_prof_users[0], "title": "Professeur",             "bio": "Spécialiste en bases de données et systèmes distribués.",     "photo_url": "https://i.pravatar.cc/150?img=11", "department": dept_info},
    {"user": created_prof_users[1], "title": "Maître de conférences A","bio": "Experte en intelligence artificielle et apprentissage automatique.", "photo_url": "https://i.pravatar.cc/150?img=5",  "department": dept_info},
    {"user": created_prof_users[2], "title": "Maître de conférences B","bio": "Spécialisé en algorithmique avancée et théorie des graphes.", "photo_url": "https://i.pravatar.cc/150?img=15", "department": dept_math},
    {"user": created_prof_users[3], "title": "Professeur",             "bio": "Spécialiste des architectures microservices et du développement agile.", "photo_url": "https://i.pravatar.cc/150?img=9",  "department": dept_si},
    {"user": created_prof_users[4], "title": "Maître assistant A",     "bio": "Expert en sécurité informatique et cryptographie.",           "photo_url": "https://i.pravatar.cc/150?img=20", "department": dept_reseau},
    {"user": created_prof_users[5], "title": "Maître de conférences A","bio": "Spécialiste des réseaux sans fil et protocoles IoT.",         "photo_url": "https://i.pravatar.cc/150?img=32", "department": dept_reseau},
    {"user": created_prof_users[6], "title": "Professeur",             "bio": "Systèmes d'exploitation et architectures matérielles.",       "photo_url": "https://i.pravatar.cc/150?img=17", "department": dept_info},
    {"user": created_prof_users[7], "title": "Maître de conférences B","bio": "Analyse de données et visualisation.",                        "photo_url": "https://i.pravatar.cc/150?img=44", "department": dept_math},
]

created_professors = []
for p in professors:
    prof = Professor.objects.create(**p)
    created_professors.append(prof)

print("Création des cours...")
courses_data = [
    {"name": "Bases de données",             "code": "INFO301",  "credits": 6, "description": "Modélisation relationnelle, SQL, normalisation.", "department": dept_info,   "professor": created_professors[0]},
    {"name": "Systèmes d'exploitation",      "code": "INFO201",  "credits": 5, "description": "Gestion des processus, mémoire, fichiers.",        "department": dept_info,   "professor": created_professors[6]},
    {"name": "Programmation orientée objet", "code": "INFO102",  "credits": 4, "description": "POO en Java : héritage, polymorphisme, patterns.", "department": dept_info,   "professor": created_professors[1]},
    {"name": "Génie logiciel",               "code": "INFO401",  "credits": 5, "description": "Méthodes agiles, UML, tests logiciels.",            "department": dept_info,   "professor": created_professors[3]},
    {"name": "Intelligence artificielle",    "code": "INFO501",  "credits": 6, "description": "Réseaux de neurones et apprentissage automatique.", "department": dept_info,   "professor": created_professors[1]},
    {"name": "Algorithmique avancée",        "code": "MINFO301", "credits": 5, "description": "Complexité, graphes, programmation dynamique.",     "department": dept_math,   "professor": created_professors[2]},
    {"name": "Mathématiques discrètes",      "code": "MINFO101", "credits": 4, "description": "Logique, ensembles, combinatoire, graphes.",        "department": dept_math,   "professor": created_professors[7]},
    {"name": "Analyse numérique",            "code": "MINFO201", "credits": 4, "description": "Méthodes numériques et interpolation.",             "department": dept_math,   "professor": created_professors[2]},
    {"name": "Probabilités et statistiques", "code": "MINFO202", "credits": 3, "description": "Variables aléatoires et tests d'hypothèses.",       "department": dept_math,   "professor": created_professors[7]},
    {"name": "Réseaux informatiques",        "code": "RT201",    "credits": 5, "description": "TCP-IP, protocoles, routage et commutation.",        "department": dept_reseau, "professor": created_professors[5]},
    {"name": "Sécurité informatique",        "code": "RT301",    "credits": 5, "description": "Cryptographie, pare-feu, VPN, cybersécurité.",       "department": dept_reseau, "professor": created_professors[4]},
    {"name": "Réseaux sans fil & IoT",       "code": "RT401",    "credits": 4, "description": "Wi-Fi, Bluetooth, MQTT et CoAP.",                   "department": dept_reseau, "professor": created_professors[5]},
    {"name": "Administration systèmes",      "code": "RT202",    "credits": 4, "description": "Linux/Windows Server, Docker et virtualisation.",    "department": dept_reseau, "professor": created_professors[4]},
    {"name": "Développement web avancé",     "code": "SI301",    "credits": 5, "description": "REST, Django, React, déploiement cloud.",            "department": dept_si,     "professor": created_professors[3]},
    {"name": "Entrepôts de données",         "code": "SI401",    "credits": 5, "description": "Data warehouse, ETL, OLAP, BI.",                    "department": dept_si,     "professor": created_professors[0]},
    {"name": "Systèmes d'information",       "code": "SI201",    "credits": 4, "description": "MERISE, UML, audit et gouvernance des SI.",          "department": dept_si,     "professor": created_professors[3]},
]

created_courses = []
for c in courses_data:
    course = Course.objects.create(**c)
    created_courses.append(course)

# Référence rapide par code
courses_by_code = {c.code: c for c in created_courses}

print("Création des actualités...")
from django.utils import timezone
from datetime import timedelta, date

news_items = [
    {"title": "Ouverture des inscriptions — Master Informatique 2024/2025", "content": "Les inscriptions pour le Master en Informatique sont officiellement ouvertes. Dépôt des dossiers avant le 30 septembre 2024.", "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800", "is_featured": True},
    {"title": "Conférence internationale sur l'IA — Appel à communications", "content": "La faculté organise sa 5ème conférence internationale sur l'IA. Soumission avant le 15 octobre 2024.", "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800", "is_featured": True},
    {"title": "Résultats des examens — Session principale",                  "content": "Les résultats sont disponibles sur l'espace étudiant. Réclamations du 10 au 15 juillet 2024.", "image_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800", "is_featured": False},
    {"title": "Hackathon étudiant — Innovation & Tech 2024",                 "content": "Hackathon de 48h sur les solutions numériques pour la ville intelligente. Équipes de 3 à 5.", "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800", "is_featured": True},
    {"title": "Nouveau laboratoire de cybersécurité inauguré",               "content": "La faculté inaugure son labo cybersécurité avec Kali Linux, Wireshark et Metasploit.", "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800", "is_featured": False},
    {"title": "Partenariat avec Algérie Télécom",                            "content": "Convention signée pour l'accueil de stagiaires et le co-encadrement de PFE.", "image_url": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800", "is_featured": False},
    {"title": "Planning des soutenances de PFE — Promotion 2024",            "content": "Les soutenances se dérouleront du 1er au 20 juillet 2024.", "image_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800", "is_featured": False},
    {"title": "Atelier Python & Data Science — Inscription ouverte",         "content": "Atelier intensif 3 jours : Pandas, NumPy, Matplotlib, Scikit-learn. Places limitées.", "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800", "is_featured": True},
]
for n in news_items:
    News.objects.create(**n)

print("Création des étudiants...")
students_data = [
    {"username": "amrani.sofiane",   "first_name": "Sofiane",  "last_name": "Amrani"},
    {"username": "belkacem.yasmine", "first_name": "Yasmine",  "last_name": "Belkacem"},
    {"username": "cherif.ilyes",     "first_name": "Ilyes",    "last_name": "Cherif"},
    {"username": "daoud.rania",      "first_name": "Rania",    "last_name": "Daoud"},
    {"username": "fekir.mehdi",      "first_name": "Mehdi",    "last_name": "Fekir"},
    {"username": "ghali.imane",      "first_name": "Imane",    "last_name": "Ghali"},
    {"username": "hamza.walid",      "first_name": "Walid",    "last_name": "Hamza"},
    {"username": "idris.sarah",      "first_name": "Sarah",    "last_name": "Idris"},
    {"username": "jelloul.adam",     "first_name": "Adam",     "last_name": "Jelloul"},
    {"username": "kamel.lyna",       "first_name": "Lyna",     "last_name": "Kamel"},
]

created_students = []
for s in students_data:
    user = User.objects.create_user(
        username=s["username"],
        first_name=s["first_name"],
        last_name=s["last_name"],
        email=f"{s['username']}@etu.faculte-info.dz",
        password="etudiant@2024",
        is_student=True,
        is_active=True,
    )
    created_students.append(user)

# ─────────────────────────────────────────────────────────
# INSCRIPTIONS AUX COURS
# Chaque étudiant est inscrit à un groupe de cours logique
# ─────────────────────────────────────────────────────────
print("Création des inscriptions...")

# Cours INFO (groupe principal)
info_courses = ["INFO301", "INFO201", "INFO102", "INFO401", "INFO501"]
# Cours MINFO
math_courses  = ["MINFO301", "MINFO101", "MINFO201", "MINFO202"]
# Cours RT
rt_courses    = ["RT201", "RT301", "RT202"]
# Cours SI
si_courses    = ["SI301", "SI201"]

# Sofiane, Ilyes, Mehdi, Walid, Adam → INFO + MINFO
for student in [created_students[0], created_students[2], created_students[4], created_students[6], created_students[8]]:
    for code in info_courses + math_courses[:2]:
        Enrollment.objects.create(student=student, course=courses_by_code[code])

# Yasmine, Rania, Imane, Sarah, Lyna → SI + RT
for student in [created_students[1], created_students[3], created_students[5], created_students[7], created_students[9]]:
    for code in si_courses + rt_courses[:2]:
        Enrollment.objects.create(student=student, course=courses_by_code[code])

# ─────────────────────────────────────────────────────────
# PLANNING DES ÉPREUVES
# ─────────────────────────────────────────────────────────
print("Création du planning des épreuves...")
from datetime import datetime
import pytz

tz = timezone.get_current_timezone()

exams_data = [
    # DS (Devoirs Surveillés) — semaine prochaine
    {"course": courses_by_code["INFO301"],  "exam_type": "DS",    "date": timezone.now() + timedelta(days=3),  "duration_minutes": 90,  "room": "Amphi A", "notes": "Cours fermé. Calculatrice autorisée."},
    {"course": courses_by_code["INFO201"],  "exam_type": "DS",    "date": timezone.now() + timedelta(days=5),  "duration_minutes": 90,  "room": "Salle 12", "notes": "QCM + exercices."},
    {"course": courses_by_code["INFO102"],  "exam_type": "DS",    "date": timezone.now() + timedelta(days=7),  "duration_minutes": 120, "room": "Labo 3",   "notes": "Examen sur machine."},
    {"course": courses_by_code["MINFO301"], "exam_type": "DS",    "date": timezone.now() + timedelta(days=4),  "duration_minutes": 90,  "room": "Salle 08", "notes": "Documents autorisés."},
    {"course": courses_by_code["RT201"],    "exam_type": "DS",    "date": timezone.now() + timedelta(days=6),  "duration_minutes": 90,  "room": "Salle 15", "notes": "Cours fermé."},
    {"course": courses_by_code["SI301"],    "exam_type": "DS",    "date": timezone.now() + timedelta(days=8),  "duration_minutes": 120, "room": "Labo 1",   "notes": "Examen sur machine. Framework Django."},

    # Examens Finaux — dans 3 semaines
    {"course": courses_by_code["INFO301"],  "exam_type": "FINAL", "date": timezone.now() + timedelta(days=21), "duration_minutes": 180, "room": "Amphi A",  "notes": "Cours fermé. Toutes sections."},
    {"course": courses_by_code["INFO501"],  "exam_type": "FINAL", "date": timezone.now() + timedelta(days=23), "duration_minutes": 180, "room": "Amphi B",  "notes": "Cours fermé."},
    {"course": courses_by_code["MINFO101"], "exam_type": "FINAL", "date": timezone.now() + timedelta(days=22), "duration_minutes": 120, "room": "Salle 10", "notes": "Documents autorisés."},
    {"course": courses_by_code["RT301"],    "exam_type": "FINAL", "date": timezone.now() + timedelta(days=25), "duration_minutes": 120, "room": "Salle 14", "notes": "QCM + étude de cas."},
    {"course": courses_by_code["SI401"],    "exam_type": "FINAL", "date": timezone.now() + timedelta(days=24), "duration_minutes": 150, "room": "Amphi C",  "notes": "Cours fermé."},
    {"course": courses_by_code["INFO401"],  "exam_type": "FINAL", "date": timezone.now() + timedelta(days=26), "duration_minutes": 120, "room": "Salle 06", "notes": "Rapport de projet à rendre."},

    # Contrôles TP
    {"course": courses_by_code["INFO102"],  "exam_type": "TP",    "date": timezone.now() + timedelta(days=10), "duration_minutes": 60,  "room": "Labo 3",   "notes": "TP noté Java."},
    {"course": courses_by_code["RT201"],    "exam_type": "TP",    "date": timezone.now() + timedelta(days=12), "duration_minutes": 60,  "room": "Labo Réseau", "notes": "Configuration Cisco Packet Tracer."},
    {"course": courses_by_code["SI301"],    "exam_type": "TP",    "date": timezone.now() + timedelta(days=14), "duration_minutes": 90,  "room": "Labo 1",   "notes": "Projet Django à démontrer."},
]

for e in exams_data:
    Exam.objects.create(**e)

# ─────────────────────────────────────────────────────────
# NOTES DES ÉTUDIANTS
# ─────────────────────────────────────────────────────────
print("Création des notes...")

# Notes pour les étudiants INFO (Sofiane, Ilyes, Mehdi, Walid, Adam)
info_students = [created_students[0], created_students[2], created_students[4], created_students[6], created_students[8]]

grades_info = [
    # (code_cours, exam_type, [notes par étudiant], coefficient, date)
    ("INFO301", "DS",    [14.5, 12.0, 16.0, 11.5, 13.0], 1.0, date(2024, 11, 10)),
    ("INFO301", "TP",    [15.0, 13.5, 17.0, 12.0, 14.0], 0.5, date(2024, 11, 20)),
    ("INFO201", "DS",    [13.0, 15.5, 12.5, 10.0, 16.5], 1.0, date(2024, 11, 12)),
    ("INFO102", "DS",    [16.0, 14.0, 11.0, 13.5, 15.0], 1.0, date(2024, 11, 14)),
    ("INFO102", "TP",    [17.0, 15.0, 12.0, 14.0, 16.0], 0.5, date(2024, 11, 22)),
    ("INFO401", "DS",    [12.5, 13.0, 14.5, 11.0, 10.5], 1.0, date(2024, 11, 16)),
    ("INFO501", "DS",    [15.5, 11.5, 13.0, 16.0, 12.0], 1.0, date(2024, 11, 18)),
    ("MINFO301","DS",    [11.0, 14.0, 10.5, 12.5, 13.5], 1.0, date(2024, 11, 11)),
    ("MINFO101","DS",    [13.5, 12.0, 15.0, 11.5, 14.5], 1.0, date(2024, 11, 13)),
]

for code, exam_type, notes, coeff, exam_date in grades_info:
    course = courses_by_code.get(code)
    if not course:
        continue
    for i, student in enumerate(info_students):
        # Vérifie que l'étudiant est inscrit à ce cours
        if Enrollment.objects.filter(student=student, course=course).exists():
            Grade.objects.create(
                student=student,
                course=course,
                exam_type=exam_type,
                value=notes[i],
                coefficient=coeff,
                date=exam_date,
            )

# Notes pour les étudiants SI/RT (Yasmine, Rania, Imane, Sarah, Lyna)
si_students = [created_students[1], created_students[3], created_students[5], created_students[7], created_students[9]]

grades_si = [
    ("SI301",  "DS",    [14.0, 16.5, 13.0, 15.5, 12.0], 1.0, date(2024, 11, 10)),
    ("SI301",  "TP",    [15.0, 17.0, 14.0, 16.0, 13.0], 0.5, date(2024, 11, 21)),
    ("SI201",  "DS",    [13.5, 12.5, 15.0, 11.0, 14.0], 1.0, date(2024, 11, 12)),
    ("RT201",  "DS",    [12.0, 14.5, 11.5, 13.0, 15.5], 1.0, date(2024, 11, 14)),
    ("RT201",  "TP",    [13.0, 15.0, 12.0, 14.0, 16.0], 0.5, date(2024, 11, 23)),
    ("RT301",  "DS",    [11.5, 13.0, 16.0, 12.5, 14.5], 1.0, date(2024, 11, 16)),
]

for code, exam_type, notes, coeff, exam_date in grades_si:
    course = courses_by_code.get(code)
    if not course:
        continue
    for i, student in enumerate(si_students):
        if Enrollment.objects.filter(student=student, course=course).exists():
            Grade.objects.create(
                student=student,
                course=course,
                exam_type=exam_type,
                value=notes[i],
                coefficient=coeff,
                date=exam_date,
            )

# ─────────────────────────────────────────────────────────
# ABSENCES
# ─────────────────────────────────────────────────────────
print("Création des absences...")

absences_data = [
    # (étudiant, code_cours, date, justifiée, raison)
    # Sofiane
    (created_students[0], "INFO301", date(2024, 10, 15), False, ""),
    (created_students[0], "INFO201", date(2024, 10, 22), True,  "Certificat médical"),
    (created_students[0], "INFO102", date(2024, 11, 5),  False, ""),

    # Yasmine
    (created_students[1], "SI301",   date(2024, 10, 14), True,  "Participation conférence"),
    (created_students[1], "RT201",   date(2024, 10, 28), False, ""),

    # Ilyes
    (created_students[2], "INFO501", date(2024, 10, 16), False, ""),
    (created_students[2], "INFO401", date(2024, 11, 6),  True,  "Convocation administrative"),
    (created_students[2], "MINFO301",date(2024, 11, 12), False, ""),

    # Rania
    (created_students[3], "SI201",   date(2024, 10, 17), True,  "Certificat médical"),
    (created_students[3], "RT201",   date(2024, 11, 7),  False, ""),

    # Mehdi
    (created_students[4], "INFO301", date(2024, 10, 18), False, ""),
    (created_students[4], "INFO102", date(2024, 10, 25), False, ""),
    (created_students[4], "INFO201", date(2024, 11, 8),  True,  "Décès famille"),

    # Imane
    (created_students[5], "SI301",   date(2024, 10, 21), False, ""),
    (created_students[5], "RT301",   date(2024, 11, 4),  True,  "Certificat médical"),

    # Walid
    (created_students[6], "INFO501", date(2024, 10, 23), False, ""),
    (created_students[6], "MINFO101",date(2024, 11, 6),  False, ""),

    # Sarah
    (created_students[7], "RT201",   date(2024, 10, 24), True,  "Participation tournoi sportif"),
    (created_students[7], "SI301",   date(2024, 11, 5),  False, ""),

    # Adam
    (created_students[8], "INFO301", date(2024, 10, 29), False, ""),
    (created_students[8], "INFO401", date(2024, 11, 9),  True,  "Certificat médical"),

    # Lyna
    (created_students[9], "SI201",   date(2024, 10, 30), False, ""),
    (created_students[9], "RT301",   date(2024, 11, 10), False, ""),
]

for student, code, abs_date, justified, reason in absences_data:
    course = courses_by_code.get(code)
    if not course:
        continue
    if Enrollment.objects.filter(student=student, course=course).exists():
        Absence.objects.create(
            student=student,
            course=course,
            date=abs_date,
            justified=justified,
            reason=reason,
        )

print("Création du compte superadmin...")
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@faculte-info.dz",
        password="admin@2024",
        first_name="Super",
        last_name="Admin",
    )

print("\n==========================================")
print("CHARGEMENT TERMINÉ AVEC SUCCÈS !")
print("==========================================")
print(f"  Départements : {Department.objects.count()}")
print(f"  Professeurs  : {Professor.objects.count()}")
print(f"  Cours        : {Course.objects.count()}")
print(f"  Actualités   : {News.objects.count()}")
print(f"  Étudiants    : {User.objects.filter(is_student=True).count()}")
print(f"  Inscriptions : {Enrollment.objects.count()}")
print(f"  Notes        : {Grade.objects.count()}")
print(f"  Absences     : {Absence.objects.count()}")
print(f"  Épreuves     : {Exam.objects.count()}")
print(f"  Admins       : {User.objects.filter(is_superuser=True).count()}")
print("\nComptes créés :")
print("  Admin    : admin / admin@2024")
print("  Prof ex. : benali.karim / prof@2024")
print("  Étud ex. : amrani.sofiane / etudiant@2024")
print("==========================================")
