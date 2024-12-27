from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.db.models import Count, Q, Avg
from django.contrib.auth.models import User
import requests # TODO: use to get book information from OpenLibrary
from .models import UserReview, ReviewReception, Badge, ObtainedBadge
from .serializers import (ReviewSerializer, UserSerializer, ReviewReceptionSerializer,
                          BadgeSerializer, ObtainedBageSerializer)
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

class ReviewReceptionView(viewsets.ModelViewSet):
    serializer_class = ReviewReceptionSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        review_id = request.data.get('review')
        reaction = request.data.get('reaction')

        if not review_id or not reaction:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            review = UserReview.objects.get(id=review_id)
        except UserReview.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        existing_reaction = ReviewReception.objects.filter(review=review, user=user).first()

        if existing_reaction:
            existing_reaction.reaction = reaction
            existing_reaction.save()
        else:
            ReviewReception.objects.create(review=review, reaction=reaction, user=user)

        return Response({'message': 'Reaction created successfully'}, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        reception_id = kwargs.get('pk')

        if not reception_id:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reception = ReviewReception.objects.get(id=reception_id)
        except ReviewReception.DoesNotExist:
            return Response({'error': 'Reaction not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if reception.user != request.user:
            return Response({'error': 'You are not authorized to delete this reaction'}, status=status.HTTP_403_FORBIDDEN)

        reception.delete()
        return Response({'message': 'Reaction deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class ObtainedBadgeView(generics.ListAPIView):
    serializer_class = ObtainedBageSerializer
    
    def get_queryset(self):
        return ObtainedBadge.objects.filter(user=self.request.user)

class SearchView(generics.ListAPIView):
    
    def get(self, request):
        query = request.query_params.get('q', '')
        page = request.query_params.get('page', 1)

        url = f'https://openlibrary.org/search.json?q={query}+computer+programming+software&limit=20&page={page}'
        response = requests.get(url)
        books = response.json().get('docs', [])
        
        books_list = []

        for book in books:
            title = book.get('title', '')
            cover_edition_key = book.get('cover_edition_key', '')
            key = book.get('key', '')
            author_name = ', '.join(book.get('author_name', []))
            first_publish_year = book.get('first_publish_year', '')
            rating = UserReview.objects.filter(book=key).aggregate(avg_rating=Avg('rating'))
            avg_rating = rating.get('avg_rating') or 'No ratings yet'

            books_list.append({
                'title': title,
                'cover_edition_key': cover_edition_key,
                'key': key,
                'author_name': author_name,
                'first_publish_year': first_publish_year,
                'rating': avg_rating
            })

        return Response(books_list)

class BookDetailView(generics.RetrieveAPIView):
    
    def get(self, request):
        key = request.query_params.get('key', '')

        url = f'https://openlibrary.org{key}.json'
        response = requests.get(url)
        book = response.json()
        
        return Response(book)