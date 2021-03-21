from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from .models import Document

class OpenapiListView(LoginRequiredMixin, ListView):
    model = Document
    context_object_name = 'apis'
    paginate_by = 10

api_list_view = OpenapiListView.as_view()

class OpenapiDetailView(LoginRequiredMixin, DetailView):
    model = Document
    context_object_name = 'api'

api_detail_view = OpenapiDetailView.as_view()

class OpenapiTaggedView(LoginRequiredMixin, ListView):
    context_object_name = 'apis'
    paginate_by = 10
    template_name = 'document_list.html'

    def get_queryset(self):
        slug = self.kwargs.get('tag', None)
        if slug:
            tag = get_object_or_404(Tag, slug=slug)
            return Document.objects.filter(tags=tag)
        else:
            return Document.objects.none()

api_tagged_view = OpenapiTaggedView.as_view()