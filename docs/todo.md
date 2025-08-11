# tasks:
- [ ] an endpoint for uploading the markdown format file
- [ ] an endpoint for text processing or checking grammar for that file
- [ ] an endpoint for retrieving the note

- [x] python manage.py startapp notes
- [x] Install, drf to settings, install markdown library
- [ ] set up view for the api
    - [ ] set up api for upload: api/notes/upload/
    - [ ] set up api for text processing:
            api/notes/grammar-check/ -> link this to the api for public language-tool
    - [ ] set up  api for retriving the notes saved
- [ ] set up url for the views of notes app
- [ ] set up url of notes app to the main notes_taking/urls
- [ ] test the url
