from decimal import Decimal
from django.db.models import Q, F
from django.db import transaction
from rest_framework import serializers
from songBank.settings import base_settings
from .models import AudioSongFile, Category, Customer, DocumentSongFile, Language, Notation, PreviewImage, Song


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class NotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notation
        fields = ['id', 'title', 'slug']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'title', 'slug']


class PreviewImageSerializer(serializers.ModelSerializer):
    # preview_image_url = serializers.SerializerMethodField()
    def create(self, validated_data):
        song_id = self.context['song_id']
        return PreviewImage.objects.create(song_id=song_id, **validated_data)

    class Meta:
        model = PreviewImage
        fields = ['id', 'preview_image']

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
    notation = NotationSerializer()
    category = CategorySerializer()
    preview_image = PreviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'title', 'author_name', 'notation', 'description', 'slug',
                  'category', 'document_files', 'metacritic', 'audio_files', 'views', 'likes', 'language', 'lyrics', 'preview_image']


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = base_settings.AUTH_USER_MODEL


class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField()
    country = serializers.CharField()

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone',
                  'country', 'birth_date', 'membership']
