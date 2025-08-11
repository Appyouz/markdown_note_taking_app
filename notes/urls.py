from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoteViewSet

# create a router instance
router = DefaultRouter()

# Register the viewset with the router
# where the first argument 'notes' is the URL prefix for this viewset
router.register(r'notes', NoteViewSet, basename='notes')

app_name = 'notes'
urlpatterns = router.urls
