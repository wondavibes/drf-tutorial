from rest_framework import generics
from rest_framework.response import Response
from notes.models import Note
from .serializers import NoteV2Serializer
from notes.permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


class NoteListCreateV2View(generics.ListCreateAPIView):
    serializer_class = NoteV2Serializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):  # type: ignore
        user = self.request.user
        if user.is_staff:
            return Note.objects.all()
        return Note.objects.filter(owner=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(
            {"status": "success", "count": queryset.count(), "data": serializer.data}
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
