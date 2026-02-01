import django_filters
from notes.models import Note


class NoteFilter(django_filters.FilterSet):
    """custom filter to filter notes by creation date"""

    created_date = django_filters.DateFilter(
        field_name="created_at", lookup_expr="date"
    )

    class Meta:
        model = Note
        fields = ["created_date"]
