import django_filters

from .models import Book
from django.db.models import Q


class BookListFilter(django_filters.FilterSet):
    is_borrowed = django_filters.BooleanFilter(method="filter_is_borrowed")

    class Meta:
        model = Book
        fields = []

    def filter_is_borrowed(self, queryset, name, value):  # noqa: ARG002
        return queryset.filter(~Q(borrowed_by__isnull=value, borrowed_on__isnull=value))
