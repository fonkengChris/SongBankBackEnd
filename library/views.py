from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

    queryset = Song.objects.prefetch_related(
        'document_files').prefetch_related('audio_files').all()
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

    # def create(self, request, *args, **kwargs):
    #     pdf_file = request.FILES.get('pdf_file')
    #     if pdf_file:
    #         # Save the uploaded PDF file to a temporary file
    #         with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    #             for chunk in pdf_file.chunks():
    #                 temp_file.write(chunk)
    #         # Generate a preview image from the PDF file
    #         with tempfile.TemporaryDirectory() as temp_dir:
    #             images = convert_from_path(
    #                 temp_file.name, output_folder=temp_dir)
    #             preview_image_path = os.path.join(temp_dir, 'preview.jpg')
    #             images[0].save(preview_image_path, 'JPEG')
    #             # Create a new instance of MyModel and save it
    #             mymodel = DocumentSongFile(
    #                 document_file=pdf_file, preview_image=preview_image_path)
    #             mymodel.save()
    #             # Serialize the new instance and return it in the response
    #             serializer = self.get_serializer(mymodel)
    #             return Response(serializer.data)
    #     else:
    #         return Response({'error': 'No PDF file was uploaded'}, status=400)


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
