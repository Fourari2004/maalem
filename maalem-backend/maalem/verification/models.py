from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class VerificationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('in_review', 'En cours de vérification'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    )

    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'},
        related_name='verification_requests'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviewed_verifications'
    )
    notes = models.TextField(blank=True)

class ProfessionalDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = (
        ('id', 'Pièce d\'identité'),
        ('business_reg', 'Registre du commerce'),
        ('tax_cert', 'Attestation fiscale'),
        ('insurance', 'Attestation d\'assurance'),
        ('qualification', 'Certificat de qualification'),
        ('diploma', 'Diplôme'),
        ('other', 'Autre'),
    )

    verification_request = models.ForeignKey(
        VerificationRequest,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='verification_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)

class Certification(models.Model):
    LEVEL_CHOICES = (
        ('basic', 'Basique'),
        ('advanced', 'Avancé'),
        ('expert', 'Expert'),
        ('master', 'Maître artisan'),
    )

    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'},
        related_name='certifications'
    )
    title = models.CharField(max_length=200)
    issuing_body = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    certificate_number = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    certificate_file = models.FileField(upload_to='certifications/')
    is_verified = models.BooleanField(default=False)
    skills = models.ManyToManyField('Skill')

    @property
    def is_valid(self):
        from django.utils import timezone
        if not self.expiry_date:
            return self.is_verified
        return self.is_verified and self.expiry_date >= timezone.now().date()

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class VerificationBadge(models.Model):
    BADGE_TYPE_CHOICES = (
        ('identity', 'Identité vérifiée'),
        ('professional', 'Professionnel vérifié'),
        ('expert', 'Expert certifié'),
        ('top_rated', 'Hautement noté'),
        ('premium', 'Artisan premium'),
    )

    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'},
        related_name='badges'
    )
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPE_CHOICES)
    awarded_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    criteria_met = models.TextField()  # JSON field storing the criteria met for this badge

    class Meta:
        unique_together = ('artisan', 'badge_type')