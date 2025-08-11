from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_503_SERVICE_UNAVAILABLE, HTTP_404_NOT_FOUND
from rest_framework.views import Response
from requests.exceptions import RequestException, HTTPError
from .models import Notes
from .serializers import NoteSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
import markdown
import requests

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
        try:
            # get note by id
            uploaded_note = Notes.objects.get(pk=pk)

            # Convert its content to HTML using markdown
            html = markdown.markdown(uploaded_note.content)

            return Response({'html_content': html}, status=HTTP_200_OK)
        except Notes.DoesNotExist:
            return Response({"detail": "Note not found."}, status=HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['get'])
    def grammar_check(self, request, pk=None):
        try:
            # Get the notes by id
            uploaded_note = Notes.objects.get(pk=pk)

            # Extract the content from the note
            extracted_content = uploaded_note.content 


            # Create a dictionary for data with required parameters
            data = {
                'text': extracted_content,
                'language': 'en-US',
            }

            # Use the request library to send this content to a grammar check API
            r = requests.post('https://api.languagetool.org/v2/check', data=data)
            
            # check if the request was sucessful
            r.raise_for_status()
            
            # Process the response from the API
            # get the JSON content from the response
            results = r.json()
            return Response(results, status=HTTP_200_OK)

        except Notes.DoesNotExist:
            return Response({"detail": "Note not found."}, status=HTTP_404_NOT_FOUND)
        except HTTPError as e:
            # Handle specific HTTP errors from the API
            return Response({"detail": f"LanguageTool API Error: {e.response.text}"}, status=e.response.status_code)
        except RequestException:
            # Handle network errors, e.g., API is down
            return Response({"detail": "Could not connect to the LanguageTool API."}, status=HTTP_503_SERVICE_UNAVAILABLE)




