from rest_framework import generics
from .serializers import NoteSerializer
from notes.models import Note
from rest_framework.permissions import IsAuthenticated
from notes.permissions import IsOwnerOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from notes.jwt import CustomTokenObtainPairSerializer


class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # type: ignore
        if self.request.user.is_staff:
            return Note.objects.all()

        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):  # type: ignore
        if self.request.user.is_staff:
            return Note.objects.all()

        return Note.objects.filter(owner=self.request.user)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
