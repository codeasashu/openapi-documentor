from django.db.models import Q
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from openapi_documentor.openapi.models import Document
from .serializer import DocumentSerializer, DocumentSpecSerializer

class OpenapiListView(ListModelMixin, GenericAPIView):
    """
    Get openapi documents in json format.
    """

    serializer_class = DocumentSerializer

    def get_queryset(self):
        term = self.request.query_params.get('search', None)
        if not term:
            return Document.objects.all()
        return Document.objects.filter(
            Q(title__icontains=term)
            | Q(tags__slug__in=[term])
        ).distinct()
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class OpenapiDetailView(RetrieveModelMixin, GenericAPIView):
    """
    Get an openapi document in json format.
    """

    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OpenapiSpecView(OpenapiDetailView):
    """
    Get an openapi spec in json format.
    """
    serializer_class = DocumentSpecSerializer