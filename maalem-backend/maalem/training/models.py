from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
        ('expert', 'Expert'),
    )

    title = models.CharField(max_length=200)
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'},
        related_name='courses_taught'
    )
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    prerequisites = models.TextField(blank=True)
    duration_hours = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_students = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_online = models.BooleanField(default=False)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    duration_hours = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

class CourseResource(models.Model):
    RESOURCE_TYPE_CHOICES = (
        ('video', 'Vidéo'),
        ('document', 'Document'),
        ('exercise', 'Exercice'),
        ('quiz', 'Quiz'),
    )

    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    content = models.TextField()  # Pour les quiz et exercices
    file = models.FileField(upload_to='course_resources/', null=True, blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

class CourseEnrollment(models.Model):
    STATUS_CHOICES = (
        ('enrolled', 'Inscrit'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)  # Pourcentage de progression

class MentorshipProgram(models.Model):
    STATUS_CHOICES = (
        ('active', 'Actif'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    )

    mentor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'},
        related_name='mentorship_programs_as_mentor'
    )
    mentee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'},
        related_name='mentorship_programs_as_mentee'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    objectives = models.TextField()
    skills_focus = models.ManyToManyField('verification.Skill')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

class MentorshipSession(models.Model):
    SESSION_TYPE_CHOICES = (
        ('in_person', 'En personne'),
        ('online', 'En ligne'),
        ('site_visit', 'Visite de chantier'),
    )

    program = models.ForeignKey(MentorshipProgram, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES)
    topics_covered = models.TextField()
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)