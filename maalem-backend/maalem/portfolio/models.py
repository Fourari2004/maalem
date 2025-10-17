from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Portfolio(models.Model):
    artisan = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'}
    )
    introduction = models.TextField()
    years_of_experience = models.IntegerField()
    services_offered = models.TextField()
    certification_details = models.TextField(blank=True)
    work_area = models.CharField(max_length=200)
    available_hours = models.CharField(max_length=200)

class PortfolioProject(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    completion_date = models.DateField()
    client_name = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100)
    before_photos = models.ManyToManyField('PortfolioImage', related_name='before_projects')
    after_photos = models.ManyToManyField('PortfolioImage', related_name='after_projects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completion_date']

class PortfolioImage(models.Model):
    image = models.ImageField(upload_to='portfolio_images/')
    caption = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    certificate_file = models.FileField(upload_to='certificates/')
    
    class Meta:
        ordering = ['-issue_date']