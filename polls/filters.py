from rest_framework import filters


class ChoiceFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        author = request.GET.get('author')
        return queryset.filter(author=author)
