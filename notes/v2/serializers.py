from notes.models import Note
from rest_framework import serializers


class NoteV2Serializer(serializers.ModelSerializer):
    body = serializers.CharField(source="content")

    class Meta:
        model = Note
        fields = ["id", "title", "body", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Title must be at least 5 characters long"
            )

        return value

    def validate(self, data):  # type: ignore
        if data["title"] == data["content"]:
            raise serializers.ValidationError("Title must be distinct from content")

        return data
