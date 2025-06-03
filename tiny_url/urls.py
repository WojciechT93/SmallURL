from django.urls import path
from tiny_url.views import CreateTinyURLView, RetrieveOriginalURLView, ListTinyURLsView


urlpatterns = [
    path('create_tiny_url/', CreateTinyURLView.as_view(), name='create_tiny_url'),
    path('get_original_url/<str:short_code>/', RetrieveOriginalURLView.as_view(), name='get_original_url'),
    path('list_tiny_urls/', ListTinyURLsView.as_view(), name='list_tiny_urls'),
]