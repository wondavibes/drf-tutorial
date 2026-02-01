from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


@method_decorator(cache_page(60 * 5), name="dispatch")
class PublicNotesListView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer