from django.contrib import admin
from .models import UserReview, ReviewReception, Badge, ObtainedBadge

# Register your models here.
admin.site.register(Badge)
admin.site.register(UserReview)
admin.site.register(ReviewReception)
admin.site.register(ObtainedBadge)