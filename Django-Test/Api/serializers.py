import json
from .models import *
from .serializers import *
from .models import *
from django.core import serializers as serializer
from rest_framework import serializers
from collections import OrderedDict
from .serializers import *
from rest_framework.response import Response
from rest_framework import status, generics, filters


class GenZSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return result

    class Meta:
        model = sentimentSentence
        fields = '__all__'

class SentenceSentimentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return result

    class Meta:
        model = sentimentSentence
        fields = ('sentence_entities',)

class SentenceSentimentCategorySerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return result

    class Meta:
        model = sentimentSentence
        fields = ('sentence_entities','category')

class YoungSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        return result

    class Meta:
        model = young
        fields = '__all__'