from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import Response
from .models import Notes
from .serializers import NoteSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser

class NoteViewSet(ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer
    parser_classes = [MultiPartParser] # Add this line

    @action(detail=False, methods=['post'])
    def upload_file(self,request):
        uploaded_file = request.FILES['markdown_file']

        # Read the file content
        file_content = uploaded_file.read()

        # Decode content which is in bytes to a string
        decoded_content = file_content.decode('utf-8')

        # Save the notes
        note_instance = Notes.objects.create(title=uploaded_file.name, content=decoded_content)
        serializer = NoteSerializer(note_instance)
        
        return Response(serializer.data, status=HTTP_201_CREATED)




