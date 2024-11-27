from .models import UserReview, ReviewReception, Badge, ObtainedBadge

def get_user_stats(user):
    from django.db.models import Count, Q

    return {
        'reviews': user.userreview_set.count(),
        'likes_given': user.userreview_set.filter(reaction=ReviewReception.LIKE).count(),
        'dislikes_given': user.userreview_set.filter(reaction=ReviewReception.DISLIKE).count(),
        'likes_received': UserReview.objects.filter(user=user)
        .annotate(
            total_likes=Count('reviewreception', filter=Q(reviewreception__reaction=ReviewReception.LIKE)),
        ).aggregate(total=Count('total_likes'))['total'] or 0,
        '.dislikes_received': UserReview.objects.filter(user=user)
        .annotate(
            total_dislikes=Count('reviewreception', filter=Q(reviewreception__reaction=ReviewReception.DISLIKE)),
        ).aggregate(total=Count('total_dislikes'))['total'] or 0,
    }

def check_and_add_badge(user):
    user_stats = get_user_stats(user)

    earned_badges = ObtainedBadge.objects.filter(user=user).values_list('badge_obtained', flat=True)
    available_badges = Badge.objects.exclude(id__in=earned_badges)

    for badge in available_badges:
        if user_stats.get(badge.condition_type, 0) >= badge.threshold:
            ObtainedBadge.objects.create(badge_obtained=badge, user=user)
            break