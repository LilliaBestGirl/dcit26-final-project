from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class UserReview(models.Model):
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField()
    book = models.PositiveIntegerField() # ID will be from another API
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']

    def __str__(self):
        return f"Review of {self.book} by {self.user}"

class ReviewReception(models.Model):
    LIKE, DISLIKE = 'like', 'dislike'
    CHOICES = [(LIKE, 'Like'), (DISLIKE, 'Dislike')]

    reaction = models.CharField(max_length=10, choices=CHOICES) # like/dislike, helpful/not helpful
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(UserReview, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'review']

    def __str__(self):
        return f"{self.user} {self.reaction}s {self.review}"
    
class Badge(models.Model):
    # Gamification feature to encourage engagement
    BRONZE, SILVER, GOLD = 'bronze', 'silver', 'gold'
    TIER_CHOICES = [(BRONZE, 'Bronze'), (SILVER, 'Silver'), (GOLD, 'Gold')]
    CONDITION_CHOICES = [
        ('reviews', 'Number of Reviews'),
        ('likes given', 'Number of Likes Given'),
        ('likes received', 'Number of Likes Received'),
        ('dislikes given', 'Number of Dislikes Given'),
        ('dislikes received', 'Number of Dislikes Received'),
    ]

    badge_name = models.CharField(max_length=25)
    description = models.TextField()
    condition_type = models.CharField(max_length=30, choices=CONDITION_CHOICES)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    threshold = models.PositiveIntegerField()

    def __str__(self):
        return self.badge_name
    
class ObtainedBadge(models.Model):
    date_obtained = models.DateField(auto_now_add=True)
    badge_obtained = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(Badge, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['badge_obtained', 'user']

    def __str__(self):
        return f"{self.user} obtained {self.badge_obtained}"