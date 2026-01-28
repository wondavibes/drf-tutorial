from rest_framework import generics
from .serializers import NoteV1Serializer
from notes.models import Note
from rest_framework.permissions import IsAuthenticated
from notes.permissions import IsOwnerOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from notes.jwt import CustomTokenObtainPairSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteV1Serializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        "title": ["exact", "icontains"],
        "created_at": ["date", "gte", "lte"],
    }
    ordering_fields = ["title", "created_at"]
    ordering = ["created_at"]  # default ordering

    def get_queryset(self):  # type: ignore
        if self.request.user.is_staff:
            return Note.objects.all()

        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteV1Serializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):  # type: ignore
        if self.request.user.is_staff:
            return Note.objects.all()

        return Note.objects.filter(owner=self.request.user)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
