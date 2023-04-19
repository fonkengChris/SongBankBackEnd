from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from library.permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .models import AudioSongFile, Category, Customer, DocumentSongFile, Notation, PreviewImage, Review, Song
# from .filters import ProductFilter
# from .pagination import DefaultPagination
from .serializers import AudioSongFileSerialiser, CustomerSerializer, DocumentSongFileSerialiser, NotationSerializer, PreviewImageSerializer, ReviewSerializer, SongSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import tempfile
import os
from pdf2image import convert_from_path


class SongViewSet(ModelViewSet):

    serializer_class = SongSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['last_update']
    filter_backends = [DjangoFilterBackend]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):

        queryset = Song.objects.prefetch_related(
            'document_files').prefetch_related('audio_files').prefetch_related('preview_image').all()
        category = self.request.GET.get('category')
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class NotationViewSet(ModelViewSet):

    queryset = Notation.objects.all()
    serializer_class = NotationSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        return {'song_id': self.kwargs['song_pk']}

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['song_pk'])


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # unpacking tuple that generates a customer object and a boolean value
        (customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class DocumentSongFileViewSet(ModelViewSet):
    serializer_class = DocumentSongFileSerialiser
    permission_classes = [IsAdminOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_context(self):
        return {'song_id': self.kwargs['song_pk']}

    @action(detail=True)
    def get_queryset(self):
        return DocumentSongFile.objects.filter(song_id=self.kwargs['song_pk'])


class AudioSongFileViewSet(ModelViewSet):
    serializer_class = AudioSongFileSerialiser
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'song_id': self.kwargs['song_pk']}

    @action(detail=True)
    def get_queryset(self):
        return AudioSongFile.objects.filter(song_id=self.kwargs['song_pk'])


class PreviewImageViewSet(ModelViewSet):
    queryset = PreviewImage.objects.all()
    serializer_class = PreviewImageSerializer

    def get_serializer_context(self):
        return {'song_id': self.kwargs['song_pk']}

    @action(detail=True)
    def get_queryset(self):
        return PreviewImage.objects.filter(song_id=self.kwargs['song_pk'])
