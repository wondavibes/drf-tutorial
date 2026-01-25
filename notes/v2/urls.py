from django.urls import path
from .views import NoteListCreateV2View

urlpatterns = [
    path("notes/", NoteListCreateV2View.as_view(), name="notesv2-list-create"),
]
