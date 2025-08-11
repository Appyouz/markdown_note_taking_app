from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import Response
from .models import Notes
from .serializers import NoteSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import markdown

class NoteViewSet(ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer

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

    
    @action(detail=True, methods=['get'])
    def render_to_html(self, request, pk=None):
        # get note by id
        uploaded_note = Notes.objects.get(pk=pk)

        # Convert its content to HTML using markdown
        html = markdown.markdown(uploaded_note.content)

        return Response({'html_content': html}, status=HTTP_200_OK)






