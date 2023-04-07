from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views


router = routers.SimpleRouter()
router.register('songs', views.SongViewSet, basename='songs')
router.register('categories', views.CategoryViewSet)
router.register('customers', views.CustomerViewSet) 


songs_router = routers.NestedDefaultRouter(router, 'songs', lookup='song')
# products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
songs_router.register('document_files', views.DocumentSongFileViewSet, basename='document-files')
songs_router.register('audio_files', views.AudioSongFileViewSet, basename='audio-files')

#URLConf
urlpatterns = router.urls + songs_router.urls

# [
#     path('products/', views.ProductList.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
# ]