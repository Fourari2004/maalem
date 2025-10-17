from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('quote_provided', 'Devis fourni'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_projects'
    )
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artisan_projects',
        limit_choices_to={'user_type': 'artisan'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.client.username} & {self.artisan.username}"

class Quote(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Refusé'),
        ('expired', 'Expiré'),
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='quotes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    materials_included = models.BooleanField(default=True)
    validity_period = models.IntegerField(help_text="Durée de validité en jours")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProjectUpdate(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    description = models.TextField()
    percentage_complete = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='project_files/')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']