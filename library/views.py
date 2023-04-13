from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework import status
from library.permissions import FullDajngoModelPermissions, IsAdminOrReadOnly, UploadSongFilePermission, ViewCustomerHistoryPermission
from .models import AudioSongFile, Category, Customer, DocumentSongFile, Song
# from .filters import ProductFilter
# from .pagination import DefaultPagination
from .serializers import AudioSongFileSerialiser, CustomerSerializer, DocumentSongFileSerialiser, SongSerializer, CategorySerializer


class SongViewSet(ModelViewSet):
    
    queryset = Song.objects.prefetch_related('document_files').prefetch_related('audio_files').all() 
    serializer_class = SongSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['last_update']

    def get_serializer_context(self):
        return {'request': self.request}



class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    # def destroy(self, request, *args, **kwargs):
    #     category = get_object_or_404(
    #         Category.objects.annotate(
    #             psongs_count=Count('songs')), pk=kwargs['pk'])
    #     if category.songs.count() > 0:
    #         return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, 
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     return super().destroy(request, *args, **kwargs)

    
# class ReviewViewSet(ModelViewSet):

#     serializer_class = ReviewSerializer
    
#     def get_serializer_context(self):
#         return {'product_id': self.kwargs['product_pk']}

#     def get_queryset(self):
#         return Review.objects.filter(product_id=self.kwargs['product_pk'])
    


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id) #unpacking tuple that generates a customer object and a boolean value
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
    
    def get_serializer_context(self):
        return {'song_id': self.kwargs['song_pk']}
    
    @action(detail=True)
    def get_queryset(self):
        return DocumentSongFile.objects.filter(song_id=self.kwargs['song_pk'])



class AudioSongFileViewSet(ModelViewSet):
    serializer_class =AudioSongFileSerialiser
    permission_classes = [IsAdminOrReadOnly]

    
    def get_serializer_context(self):
        return {'song_id': self.kwargs['song_pk']}
    
    @action(detail=True)
    def get_queryset(self):
        return AudioSongFile.objects.filter(song_id=self.kwargs['song_pk'])

