from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

User = get_user_model()

class Schedule(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    )

    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'}
    )
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('artisan', 'day_of_week')

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être antérieure à l'heure de fin")

class TimeOff(models.Model):
    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'artisan'}
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.TextField(blank=True)

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("La date de début doit être antérieure à la date de fin")

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    )

    artisan = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='artisan_appointments',
        limit_choices_to={'user_type': 'artisan'}
    )
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='client_appointments'
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    service_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être antérieure à l'heure de fin")
        
        # Vérifier si l'artisan est disponible
        if not self.is_artisan_available():
            raise ValidationError("L'artisan n'est pas disponible à cette période")
    
    def is_artisan_available(self):
        # Vérifier l'horaire régulier
        day_of_week = self.date.weekday()
        schedule = Schedule.objects.filter(
            artisan=self.artisan,
            day_of_week=day_of_week,
            is_available=True
        ).first()
        
        if not schedule:
            return False
        
        if self.start_time < schedule.start_time or self.end_time > schedule.end_time:
            return False
        
        # Vérifier les congés
        time_off = TimeOff.objects.filter(
            artisan=self.artisan,
            start_date__lte=datetime.combine(self.date, self.end_time),
            end_date__gte=datetime.combine(self.date, self.start_time)
        ).exists()
        
        if time_off:
            return False
        
        # Vérifier les autres rendez-vous
        conflicting_appointments = Appointment.objects.filter(
            artisan=self.artisan,
            date=self.date,
            status='confirmed'
        ).exclude(id=self.id)
        
        for appointment in conflicting_appointments:
            if (self.start_time < appointment.end_time and 
                self.end_time > appointment.start_time):
                return False
        
        return True