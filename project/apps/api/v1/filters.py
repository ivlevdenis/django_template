from django_filters import BaseCSVFilter, CharFilter


class CharArrayFilter(BaseCSVFilter, CharFilter):
    pass
