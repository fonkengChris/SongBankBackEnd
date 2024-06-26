from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter()
router.register('songs', views.SongViewSet, basename='songs')
router.register('categories', views.CategoryViewSet)
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('notations', views.NotationViewSet)
router.register('languages', views.LanguageViewSet)


songs_router = routers.NestedDefaultRouter(router, 'songs', lookup='song')

songs_router.register(
    'document_files', views.DocumentSongFileViewSet, basename='document-files')
songs_router.register(
    'audio_files', views.AudioSongFileViewSet, basename='audio-files')
songs_router.register(
    'preview_image', views.PreviewImageViewSet, basename='preview-images')

urlpatterns1 = [
    path('', include(router.urls)),
    # register custom path with router
    path('like/unlike/<int:pk>/', include(router.urls)),
]

# URLConf
urlpatterns = router.urls + songs_router.urls + urlpatterns1

# print(urlpatterns)
