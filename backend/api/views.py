from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.db.models import Count, Avg, Subquery, OuterRef, Value, CharField
from django.contrib.auth.models import User
import requests
from .models import UserReview, ReviewReception, Badge
from .serializers import (ReviewSerializer, UserSerializer, ReviewReceptionSerializer,
                          BadgeSerializer)
from .utils import check_and_add_badge

# Create your views here.

class UserInfoView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class BookReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        key = self.request.query_params.get('key', '')

        is_authenticated = self.request.user.is_authenticated

        queryset = UserReview.objects.filter(book=key).annotate(
            total_likes=Subquery(
                ReviewReception.objects.filter(
                    review=OuterRef('id'), reaction=ReviewReception.LIKE
                ).values('review').annotate(count=Count('id')).values('count')[:1]
            ),
            total_dislikes=Subquery(
                ReviewReception.objects.filter(
                    review=OuterRef('id'), reaction=ReviewReception.DISLIKE
                ).values('review').annotate(count=Count('id')).values('count')[:1]
            ),
            user_reaction=Subquery(
                ReviewReception.objects.filter(
                    review=OuterRef('id'), user=self.request.user
                ).values('reaction')[:1]
            ) if is_authenticated else Value(None, output_field=CharField())
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserReview.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        check_and_add_badge(self.request.user)

class ReviewReceptionView(generics.CreateAPIView):
    serializer_class = ReviewReceptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        review_id = request.data.get('review')
        reaction = request.data.get('reaction')

        if not reaction:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        review = get_object_or_404(UserReview, id=review_id)
        existing_reaction = ReviewReception.objects.filter(review=review, user=user).first()

        if existing_reaction:
            if str(existing_reaction.reaction).strip().lower() == str(reaction).strip().lower():
                existing_reaction.delete()
                return Response({'message': 'Reaction deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                existing_reaction.reaction = reaction
                existing_reaction.save()
                return Response({'message': 'Reaction updated successfully'}, status=status.HTTP_200_OK)
        else:
            ReviewReception.objects.create(review=review, reaction=reaction, user=user)
            check_and_add_badge(user)
            return Response({'message': 'Reaction created successfully'}, status=status.HTTP_201_CREATED)

class ObtainedBadgeView(generics.ListAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Badge.objects.filter(obtainedbadge__user=self.request.user)

class SearchView(generics.ListAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        page = request.query_params.get('page', 1)

        url = f'https://openlibrary.org/search.json?q={query}+computer+programming+software&limit=20&page={page}'
        response = requests.get(url)
        total_results = response.json().get('numFound', '')
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

        rated_books = [book for book in books_list if book['rating'] != 'No ratings yet']
        unrated_books = [book for book in books_list if book['rating'] == 'No ratings yet']

        rated_books.sort(key=lambda x: x['rating'], reverse=True)
        
        sorted_results = rated_books + unrated_books

        full_results = {
            'numFound': total_results,
            'docs': sorted_results
        }

        return Response(full_results)

class BookDetailView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def get(self, request):
        key = request.query_params.get('key', '')

        url = f'https://openlibrary.org{key}.json'
        response = requests.get(url)
        book = response.json()

        details = {
            'title': book.get('title', ''),
            'cover_edition_key': book.get('cover_edition_key', ''),
            'key': book.get('key', ''),
            'author_name': ', '.join(book.get('author_name', [])),
            'first_publish_year': book.get('first_publish_year', ''),
            'description': book.get('description', ''),
            'rating': UserReview.objects.filter(book=key).aggregate(avg_rating=Avg('rating')).get('avg_rating') or 'No ratings yet'
            }
        
        return Response(details)