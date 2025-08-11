from .models import Notes
from .serializers import NoteSerializer
from rest_framework.viewsets import ModelViewSet


class NoteViewSet(ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer
