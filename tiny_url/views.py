from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from tiny_url.serializers import CreateTinyURLSerializer, TinyURLBaseSerializer
from tiny_url.models import TinyURL


class CreateTinyURLView(CreateAPIView):
    """
    View to create a TinyURL instance.
    """
    serializer_class = CreateTinyURLSerializer


class RetrieveOriginalURLView(RetrieveAPIView):
    """
    View to retrieve the original URL from a TinyURL instance.
    """
    queryset = TinyURL.objects.all()
    serializer_class = TinyURLBaseSerializer
    lookup_field = 'short_code'


class ListTinyURLsView(ListAPIView):
    """
    View to list all TinyURL instances.
    """
    queryset = TinyURL.objects.all()
    serializer_class = TinyURLBaseSerializer
