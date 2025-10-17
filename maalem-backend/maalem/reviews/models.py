from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    artisan = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='received_reviews',
        limit_choices_to={'user_type': 'artisan'}
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='given_reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    work_quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    punctuality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    professionalism = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photos = models.ManyToManyField('ReviewPhoto', blank=True)

    class Meta:
        unique_together = ('artisan', 'reviewer')
        ordering = ['-created_at']

class ReviewPhoto(models.Model):
    image = models.ImageField(upload_to='review_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review photo {self.id}"