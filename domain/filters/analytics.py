""" Filters for analytics. """
from django_filters import rest_framework as filters


class LikesAnalyticsFilterSet(filters.FilterSet):
    """ Filter set for the Likes analytics. """

    username = filters.CharFilter(field_name="user__username", lookup_expr="exact")
    post_title = filters.CharFilter(field_name="post__title", lookup_expr="exact")
    date_from = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    date_to = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
