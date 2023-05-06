import os
import tempfile

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from pdf2image import convert_from_path
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from library.permissions import (IsAdminOrReadOnly,
                                 ViewCustomerHistoryPermission)

from .models import (AudioSongFile, Category, Customer, DocumentSongFile,
                     Notation, PreviewImage,  Song)
# from .filters import ProductFilter
# from .pagination import DefaultPagination
from .serializers import (AudioSongFileSerialiser, CategorySerializer,
                          CustomerSerializer, DocumentSongFileSerialiser,
                          NotationSerializer, PreviewImageSerializer,
                          SongSerializer)


class SongViewSet(ModelViewSet):

    serializer_class = SongSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['last_update', 'title', 'metacritic']
    filter_backends = [DjangoFilterBackend]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):

        queryset = Song.objects.prefetch_related(
            'document_files').prefetch_related('audio_files').prefetch_related('preview_image').all()
        category = self.request.GET.get('category')
        notation = self.request.GET.get('notation')
        ordering = self.request.GET.get('ordering')
        slug = self.request.GET.get('slug')
        search = self.request.GET.get('search')
        if category is not None:
            queryset = queryset.filter(category=category)
        if notation is not None:
            queryset = queryset.filter(notation=notation)
        if ordering is not None:
            queryset = queryset.order_by(ordering)
        if search is not None:
            queryset = queryset.filter(Q(title__icontains=search) | Q(
                author_name__icontains=search) | Q(category__title__icontains=search))
        return queryset

    @action(detail=True, methods=['post'])
    def like_unlike(self, request, pk=None):
        post = self.get_object()
        if post.likes.filter(pk=request.user.pk).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        serializer = self.get_serializer(post)
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class NotationViewSet(ModelViewSet):

    queryset = Notation.objects.all()
    serializer_class = NotationSerializer
    permission_classes = [IsAdminOrReadOnly]


class CustomerViewSet(ModelViewSet):

    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Customer.objects.all()
        user_id = self.request.GET.get('user_id')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @action(detail=True)
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
