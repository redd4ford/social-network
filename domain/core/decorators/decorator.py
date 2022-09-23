from abc import (
    ABC,
    abstractmethod,
)

from django.db.models import (
    QuerySet,
    Model,
)


class BaseDecorator(ABC):
    """ Base decorator. """

    def __init__(self, decorating_value):
        self._decorating_value = decorating_value

    @abstractmethod
    def get(self):
        """
        Returns decorating queryset.
        """
        pass


class QuerySetDecorator(BaseDecorator):
    """ Queryset decorator to wrap raw queryset. """

    def __init__(self, decorating_value: QuerySet[Model]):
        super().__init__(decorating_value)

    def get(self):
        return self._decorating_value


class FilterDecorator(BaseDecorator):
    """ Base decorator to filter queryset. """

    filter_set_class = None

    def __init__(self, filter_set_class, decorating_value, query_params):
        super().__init__(decorating_value)
        self.__query_params = query_params
        self._filter_set_class = filter_set_class

    def get(self) -> QuerySet:
        """
        Apply filters to queryset.
        """
        queryset = self._decorating_value.get()
        fs = self._filter_set_class(self.__query_params, queryset=queryset)
        return fs.qs
