import json
from rest_framework import serializers
from openapi_documentor.openapi.models import Document, TaggedDocument


class TagListSerializer(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, instance):
        return [tag.name for tag in instance.all()]


class DocumentSerializer(serializers.ModelSerializer):
    tags = TagListSerializer()
    class Meta:
        model = Document
        fields = '__all__'
    
    def to_representation(self, instance):
        """Parse openapi doc"""
        ret = super().to_representation(instance)
        ret['formatted'] = json.loads(instance.formatted)
        return ret

class DocumentSpecSerializer(DocumentSerializer):
    class Meta:
        model = Document
        fields = ('formatted',)
    
    def to_representation(self, instance):
        return json.loads(instance.formatted)
