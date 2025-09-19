from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(
        upload_to='teachers/',
        default='teachers/default.jpg'
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"

    @property
    def image_url(self):
        if self.profile_picture and hasattr(self.profile_picture, 'url') and self.profile_picture.url:
            return self.profile_picture.url
        return '/static/images/teachers/default.jpg'

class Evaluation(models.Model):
    RATING_CHOICES = [
        (1, '1 - Muy Insatisfecho'),
        (2, '2 - Insatisfecho'),
        (3, '3 - Neutral'),
        (4, '4 - Satisfecho'),
        (5, '5 - Muy Satisfecho'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Evaluación para {self.teacher.name} - {self.rating}/5"