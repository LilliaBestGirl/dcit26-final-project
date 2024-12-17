from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from django.db.models import Count, Q
from django.contrib.auth.models import User
import requests # TODO: use to get book information from OpenLibrary
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        check_and_add_badge(self.request.user)

class BadgeView(generics.ListAPIView):
    serializer_class = Badge
    
    def get_queryset(self):
        return Badge.objects.filter(user=self.request.user)

class SearchView(generics.ListAPIView):
    
    def get(self, request, format=None):
        query = request.query_params.get('q', '')
        page = request.query_params.get('page', 1)

        url = f'https://openlibrary.org/search.json?q={query}+computer+programming+software&limit=20&page={page}'
        response = requests.get(url)
        print(response.status_code)

        books = response.json().get('docs', [])
        return Response(books)



        