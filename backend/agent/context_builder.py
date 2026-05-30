"""
agent/context_builder.py
Construit le résumé textuel de la base de données injecté dans le prompt.

- build_context(user=None) :
    * user=None  → contexte public uniquement (accessible à tous)
    * user=User  → contexte public + données personnelles de l'étudiant
"""
from faculty.models import Department, Professor, Course, News, Grade, Absence, Exam, Enrollment
from django.utils import timezone

def _mention(value: float) -> str:
    if value >= 16: return "Très Bien"
    if value >= 14: return "Bien"
    if value >= 12: return "Assez Bien"
    if value >= 10: return "Passable"
    return "Insuffisant"
# ─────────────────────────────────────────────
# CONTEXTE PUBLIC — accessible à tous
# ─────────────────────────────────────────────
def build_public_context() -> str:
    lines = []

    lines.append("=== DÉPARTEMENTS ===")
    for d in Department.objects.all():
        lines.append(f"- [{d.code}] {d.name} : {d.description}")

    lines.append("\n=== PROFESSEURS ===")
    for p in Professor.objects.select_related("department", "user").all():
        full_name = f"{p.user.first_name} {p.user.last_name}"
        lines.append(
            f"- {full_name} ({p.title}) | Département : {p.department.name} | Bio : {p.bio}"
        )

    lines.append("\n=== COURS ===")
    for c in Course.objects.select_related("department", "professor__user").all():
        prof_name = ""
        if c.professor:
            prof_name = f"{c.professor.user.first_name} {c.professor.user.last_name}"
        lines.append(
            f"- [{c.code}] {c.name} | {c.credits} crédits"
            f" | Dept : {c.department.name}"
            f" | Enseignant : {prof_name or 'Non assigné'}"
            f" | {c.description}"
        )

    lines.append("\n=== ACTUALITÉS RÉCENTES ===")
    for n in News.objects.order_by("-date")[:6]:
        lines.append(
            f"- {n.title} ({n.date.strftime('%d/%m/%Y')}) : {n.content[:200]}..."
        )

    return "\n".join(lines)


# ─────────────────────────────────────────────
# CONTEXTE PRIVÉ — données personnelles étudiant
# ─────────────────────────────────────────────
def build_student_context(user) -> str:
    lines = []
    full_name = f"{user.first_name} {user.last_name}"

    lines.append(f"\n=== DONNÉES PERSONNELLES DE L'ÉTUDIANT : {full_name} ===")

    # ── Cours inscrits ──
    enrollments = Enrollment.objects.filter(student=user).select_related(
        "course__department", "course__professor__user"
    )
    if enrollments.exists():
        lines.append("\n--- Cours auxquels je suis inscrit ---")
        for e in enrollments:
            c = e.course
            prof = ""
            if c.professor:
                prof = f"{c.professor.user.first_name} {c.professor.user.last_name}"
            lines.append(
                f"- [{c.code}] {c.name} | {c.credits} crédits"
                f" | Dept : {c.department.name}"
                f" | Enseignant : {prof or 'Non assigné'}"
            )
    else:
        lines.append("\n--- Cours : aucune inscription enregistrée ---")

    # ── Notes ──
    grades = Grade.objects.filter(student=user).select_related("course").order_by("course__code", "-date")
    if grades.exists():
        lines.append("\n--- Mes notes ---")
        for g in grades:
            lines.append(
                f"- {g.course.name} [{g.course.code}]"
                f" | {g.get_exam_type_display()} : {g.value}/20"
                f" | Coeff : {g.coefficient}"
                f" | Date : {g.date.strftime('%d/%m/%Y')}"
                f" | Mention : {_mention(g.value)}"
                + (f" | Commentaire : {g.comment}" if g.comment else "")
            )

        # Moyenne générale par cours
        lines.append("\n--- Moyennes par cours ---")
        cours_ids = enrollments.values_list("course_id", flat=True)
        for course_id in cours_ids:
            cours_grades = grades.filter(course_id=course_id)
            if cours_grades.exists():
                total_w = sum(g.value * g.coefficient for g in cours_grades)
                total_c = sum(g.coefficient for g in cours_grades)
                moyenne = total_w / total_c if total_c > 0 else 0
                course_name = cours_grades.first().course.name
                course_code = cours_grades.first().course.code
                lines.append(
                    f"- {course_name} [{course_code}] : moyenne = {moyenne:.2f}/20"
                )
    else:
        lines.append("\n--- Notes : aucune note enregistrée ---")

    # ── Absences ──
    absences = Absence.objects.filter(student=user).select_related("course").order_by("-date")
    if absences.exists():
        lines.append("\n--- Mes absences ---")
        total = absences.count()
        justified = absences.filter(justified=True).count()
        unjustified = total - justified
        lines.append(f"  Total : {total} absence(s) | Justifiées : {justified} | Non justifiées : {unjustified}")
        for a in absences:
            status = "Justifiée" if a.justified else "Non justifiée"
            lines.append(
                f"- {a.course.name} [{a.course.code}]"
                f" | {a.date.strftime('%d/%m/%Y')}"
                f" | {status}"
                + (f" | Motif : {a.reason}" if a.reason else "")
            )
    else:
        lines.append("\n--- Absences : aucune absence enregistrée ---")

    # ── Planning des épreuves (à venir) ──
    now = timezone.now()
    # Cours de l'étudiant
    enrolled_course_ids = enrollments.values_list("course_id", flat=True)
    upcoming_exams = Exam.objects.filter(
        course_id__in=enrolled_course_ids,
        date__gte=now
    ).select_related("course").order_by("date")

    if upcoming_exams.exists():
        lines.append("\n--- Mon planning des épreuves à venir ---")
        for ex in upcoming_exams:
            jours_restants = (ex.date.date() - now.date()).days
            lines.append(
                f"- {ex.course.name} [{ex.course.code}]"
                f" | {ex.get_exam_type_display()}"
                f" | Date : {ex.date.strftime('%d/%m/%Y à %H:%M')}"
                f" | Durée : {ex.duration_minutes} min"
                f" | Salle : {ex.room or 'À confirmer'}"
                f" | Dans {jours_restants} jour(s)"
                + (f" | Note : {ex.notes}" if ex.notes else "")
            )
    else:
        lines.append("\n--- Planning : aucune épreuve à venir pour vos cours ---")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# FONCTION PRINCIPALE — appelée par agent/views.py
# ─────────────────────────────────────────────
def build_context(user=None) -> str:
    """
    user=None        → contexte public uniquement
    user=User obj    → contexte public + données personnelles étudiant
    """
    context = build_public_context()

    if user is not None and user.is_authenticated and user.is_student:
        context += build_student_context(user)

    return context
