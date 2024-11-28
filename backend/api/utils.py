from .models import UserReview, ReviewReception, Badge, ObtainedBadge

def get_user_stats(user):
    from django.db.models import Count, Q, Sum

    reviews = user.userreview_set.count()

    likes_given = ReviewReception.objects.filter(user=user, reaction=ReviewReception.LIKE).count()

    dislikes_given = ReviewReception.objects.filter(user=user, reaction=ReviewReception.DISLIKE).count()

    likes_received = UserReview.objects.filter(user=user) .annotate(
        total_likes=Count('reviewreception', filter=Q(reviewreception__reaction=ReviewReception.LIKE)),
    ).aggregate(total_likes_received=Sum('total_likes'))['total_likes_received'] or 0

    dislikes_received = UserReview.objects.filter(user=user).annotate(
        total_dislikes=Count('reviewreception', filter=Q(reviewreception__reaction=ReviewReception.DISLIKE)),
    ).aggregate(total_dislikes_received=Sum('total_dislikes'))['total_dislikes_received'] or 0

    return {
        'reviews': reviews,
        'likes_given': likes_given,
        'dislikes_given': dislikes_given,
        'likes_received': likes_received,
        'dislikes_received': dislikes_received,
    }

def check_and_add_badge(user):
    user_stats = get_user_stats(user)

    earned_badges = ObtainedBadge.objects.filter(user=user).values_list('badge_obtained', flat=True)
    available_badges = Badge.objects.exclude(id__in=earned_badges)

    for badge in available_badges:
        if user_stats.get(badge.condition_type, 0) >= badge.threshold:
            ObtainedBadge.objects.create(badge_obtained=badge, user=user)
            break