from decimal import Decimal
from django.db.models import Q, F
from django.db import transaction
from rest_framework import serializers
from .models import AudioSongFile, Category, Customer, DocumentSongFile, Notation, PreviewImage, Review, Song


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class NotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notation
        fields = ['id', 'title']


class PreviewImageSerializer(serializers.ModelSerializer):
    preview_image_url = serializers.SerializerMethodField()

    class Meta:
        model = PreviewImage
        fields = '__all__'

    def get_preview_image_url(self, obj):
        if obj.preview_image:
            return obj.preview_image.url
        return None


class DocumentSongFileSerialiser(serializers.ModelSerializer):

    def create(self, validated_data):
        song_id = self.context['song_id']
        return DocumentSongFile.objects.create(song_id=song_id, **validated_data)

    class Meta:
        model = DocumentSongFile
        fields = ['id', 'document_file']


class AudioSongFileSerialiser(serializers.ModelSerializer):

    def create(self, validated_data):
        song_id = self.context['song_id']
        return AudioSongFile.objects.create(song_id=song_id, **validated_data)

    class Meta:
        model = AudioSongFile
        fields = ['id', 'audio_file']


class SongSerializer(serializers.ModelSerializer):
    document_files = DocumentSongFileSerialiser(many=True, read_only=True)
    audio_files = AudioSongFileSerialiser(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'title', 'author_name', 'description', 'slug',
                  'category', 'document_files', 'audio_files', 'preview_image', 'reviews']


class ReviewSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'date', 'description']

    def create(self, validated_data):
        song_id = self.context['song_id']
        return Review.objects.create(song_id=song_id, **validated_data)


class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']
