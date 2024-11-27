from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import UserReview, ReviewReception, Badge, ObtainedBadge
from .serializers import ReviewSerializer, UserSerializer
from .utils import check_and_add_badge

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class BookReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']

        queryset = UserReview.objects.filter(book=book_id).annotate(
            total_likes=Count('reviewreception', filter=Q(reviewreception__reaction=ReviewReception.LIKE)),
            total_dislikes=Count('reviewreception', filter=Q(reviewreception__reaction=ReviewReception.DISLIKE)),
        )

        if not queryset.exists():
            raise NotFound(detail='No reviews for this book')

        return queryset
    
class UserReviewView(viewsets.ModelViewSet):
    """
        This view will handle all CRUD operations for the UserReview model
        get_queryset() overrides the list() function, returning all reviews for the user instead of all reviews
        ModelViewSet will provide the following methods by default:
        retrieve() will return a single review
        create() will create a new review
        update() will update an existing review
        delete() will delete an existing review
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return UserReview.objects.filter(user=self.request.user)

class BadgeView(generics.ListAPIView):
    serializer_class = Badge
    
    def get_queryset(self):
        return Badge.objects.filter(user=self.request.user)