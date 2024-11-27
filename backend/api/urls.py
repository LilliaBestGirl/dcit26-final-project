from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'api/user/review', views.UserReviewView, basename='user_review')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('api/book/review/<int:book_id>/', views.BookReviewsView.as_view(), name='review'),
    path('api/user/badge/', views.BadgeView.as_view(), name='user_badge'),
]