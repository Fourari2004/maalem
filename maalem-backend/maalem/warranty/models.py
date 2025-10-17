from django.db import models
from django.contrib.auth import get_user_model
from maalem.projects.models import Project

User = get_user_model()

class Insurance(models.Model):
    INSURANCE_TYPE_CHOICES = (
        ('liability', 'Responsabilité civile'),
        ('professional', 'Assurance professionnelle'),
        ('decennial', 'Garantie décennale'),
        ('damage', 'Dommages-ouvrage'),
    )

    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'}
    )
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPE_CHOICES)
    provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    document = models.FileField(upload_to='insurance_documents/')
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('artisan', 'insurance_type', 'policy_number')

class Warranty(models.Model):
    WARRANTY_TYPE_CHOICES = (
        ('workmanship', 'Garantie travaux'),
        ('materials', 'Garantie matériaux'),
        ('equipment', 'Garantie équipements'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='warranties')
    warranty_type = models.CharField(max_length=20, choices=WARRANTY_TYPE_CHOICES)
    description = models.TextField()
    duration_months = models.IntegerField()
    start_date = models.DateField()
    conditions = models.TextField()
    exclusions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def end_date(self):
        from dateutil.relativedelta import relativedelta
        return self.start_date + relativedelta(months=self.duration_months)

    @property
    def is_active(self):
        from django.utils import timezone
        return timezone.now().date() <= self.end_date

class WarrantyClaim(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Soumise'),
        ('under_review', 'En cours d\'examen'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
        ('resolved', 'Résolue'),
    )

    warranty = models.ForeignKey(Warranty, on_delete=models.CASCADE, related_name='claims')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    resolution_date = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    cost_incurred = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class ClaimEvidence(models.Model):
    claim = models.ForeignKey(WarrantyClaim, on_delete=models.CASCADE, related_name='evidence')
    description = models.CharField(max_length=200)
    file = models.FileField(upload_to='warranty_claims/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']