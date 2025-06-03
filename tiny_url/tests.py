from django.test import TestCase
from django.db.utils import IntegrityError
from rest_framework.test import APIClient
from django.urls import reverse
from tiny_url.models import TinyURL, CHARACTERS


class TinyURLModelTests(TestCase):
    def test_creates_short_code_for_valid_url(self):
        url_instance = TinyURL.objects.create(url="https://example.com")
        self.assertIsNotNone(url_instance.short_code)
        self.assertLessEqual(len(url_instance.short_code), 10)

    def test_handles_primary_key_zero(self):
        url_instance = TinyURL.objects.create(url="https://example.com")
        url_instance.pk = 0
        url_instance.short_code = url_instance._encode_short_code()
        self.assertEqual(url_instance.short_code, CHARACTERS[0])

    def test_prevents_duplicate_url_entries(self):
        TinyURL.objects.create(url="https://example.com")
        with self.assertRaises(IntegrityError):
            TinyURL.objects.create(url="https://example.com")

    def test_prevents_duplicate_short_code_entries(self):
        url_instance = TinyURL.objects.create(url="https://example.com")
        duplicate_instance = TinyURL(url="https://example2.com", short_code=url_instance.short_code)
        with self.assertRaises(IntegrityError):
            duplicate_instance.save()

    def test_generates_different_short_codes_for_different_urls(self):
        url_instance1 = TinyURL.objects.create(url="https://example1.com")
        url_instance2 = TinyURL.objects.create(url="https://example2.com")
        self.assertNotEqual(url_instance1.short_code, url_instance2.short_code)


class CreateTinyURLViewTests(TestCase):
    def test_creates_tiny_url_instance_with_valid_url(self):
        client = APIClient()
        url = reverse('create_tiny_url')
        response = client.post(url, {'url': 'https://example.com'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('short_code', response.data)

    def test_fails_to_create_tiny_url_instance_with_invalid_url(self):
        client = APIClient()
        url = reverse('create_tiny_url')
        response = client.post(url, {'url': 'invalid-url'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('url', response.data)

    def test_fails_to_create_tiny_url_instance_with_missing_url(self):
        client = APIClient()
        url = reverse('create_tiny_url')
        response = client.post(url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('url', response.data)


class RetrieveOriginalURLViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tiny_url_instance = TinyURL.objects.create(url='https://example.com')

    def test_retrieves_original_url_for_valid_tiny_url(self):
        url = reverse('get_original_url', kwargs={'short_code': self.tiny_url_instance.short_code})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], self.tiny_url_instance.url)

    def test_fails_to_retrieve_original_url_for_invalid_tiny_url(self):
        url = reverse('get_original_url', kwargs={'short_code': 'invalid'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ListTinyURLsViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tiny_url_instance1 = TinyURL.objects.create(url='https://example1.com')
        self.tiny_url_instance2 = TinyURL.objects.create(url='https://example2.com')

    def test_lists_all_tiny_urls(self):
        url = reverse('list_tiny_urls')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn('short_code', response.data[0])
        self.assertIn('short_code', response.data[1])
