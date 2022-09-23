import copy
import datetime
from typing import (
    List,
    Union,
)

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate

from app_services import LikeService
from domain.core.decorators import (
    QuerySetDecorator,
    FilterDecorator,
)
from domain.filters.analytics import LikesAnalyticsFilterSet

User = get_user_model()


class LikeAnalyticsService:
    DATE_FORMAT = '%Y-%m-%d'

    def get_like_analytics(self, **kwargs):
        likes = LikeService().get_all()

        filter_params = copy.deepcopy(kwargs.get('query_params'))
        date_from = filter_params.get('date_from', None)
        date_to = filter_params.get('date_to', None)
        if all([date_from, date_to, date_from == date_to]):
            date_to = self._add_time_to_date_to_get_full_day(date_to)
            filter_params['date_to'] = str(date_to)

        queryset_decorator = QuerySetDecorator(likes)
        filter_decorator = FilterDecorator(
            LikesAnalyticsFilterSet,
            queryset_decorator,
            filter_params
        )

        aggregated_data = (
            filter_decorator.get()
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(likes=Count('id'))
            .order_by()
        )

        if not aggregated_data:
            aggregated_data = self._generate_zero_aggregated_data(date_from, date_to)

        return aggregated_data

    @classmethod
    def _add_time_to_date_to_get_full_day(cls, date: str):
        """
        If date_from == date_to, add timedelta to date_to in order to get all the like operations
        performed that exact day.
        """
        return (
                datetime.datetime.strptime(date, cls.DATE_FORMAT) +
                datetime.timedelta(hours=23, minutes=59, seconds=59)
        )

    def _generate_zero_aggregated_data(self, date_from: str, date_to: Union[str, datetime.datetime]):
        """
        Generate a list of dates between date_from and date_to if there were no likes during those
        days.
        """
        if all([type(date_to) == datetime.datetime, date_from == str(date_to.date())]):
            aggregated_data = [{'date': date_from, 'likes': 0}]
        else:
            dates_between = self._get_dates_between(date_from, date_to)
            aggregated_data = [{'date': date, 'likes': 0} for date in dates_between]
        return aggregated_data

    @classmethod
    def _get_dates_between(cls, date_from: str, date_to: str) -> List[str]:
        """
        Generate a list of dates between date_from and date_to.
        """
        return [
            str(datetime.datetime.strptime(date_from, cls.DATE_FORMAT) + datetime.timedelta(days=x))
            for x in range(
                (
                        datetime.datetime.strptime(date_to, cls.DATE_FORMAT) -
                        datetime.datetime.strptime(date_from, cls.DATE_FORMAT)
                ).days
            )
        ]
