# api/serializers.py
from rest_framework import serializers
from .models import TranslationRequest

class TranslationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationRequest
        fields = ['id', 'text', 'source_lang', 'target_lang', 'translated_text']
