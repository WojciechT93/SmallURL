from rest_framework import serializers

from tiny_url.models import TinyURL


class TinyURLBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for TinyURL model.

    This serializer is used to define common fields and methods for TinyURL instances.
    """
    tiny_url = serializers.SerializerMethodField()

    class Meta:
        model = TinyURL
        fields = ['url', 'tiny_url', 'short_code']
        read_only_fields = ['tiny_url', 'short_code']

    def get_tiny_url(self, obj: TinyURL) -> str | None:
        """
        Generate the full tiny URL based on the request context.

        Args:
            obj (TinyURL): The TinyURL instance for which to generate the tiny URL.

        Returns:
            str: The full tiny URL if the request context is available, otherwise None.
        """
        request = self.context.get('request')
        if request:
            protocol = 'https' if request.is_secure() else 'http'
            host = request.get_host()
            return f'{protocol}://{host}/{obj.short_code}'
        return None


class CreateTinyURLSerializer(TinyURLBaseSerializer):
    """
    Serializer for creating a TinyURL instance.

    Fields:
        url (URLField): The original URL to be shortened.
        short_code (CharField): The unique short code for the TinyURL, generated automatically.
        tiny_url (SerializerMethodField): The full tiny URL generated from the short code.
    """
    tiny_url = serializers.SerializerMethodField()

    class Meta:
        model = TinyURL
        fields = ['url', 'short_code', 'tiny_url']
        read_only_fields = ['short_code', 'tiny_url']

    def create(self, validated_data: dict) -> TinyURL:
        """
        Create a TinyURL instance and automatically generate the tiny URL.

        Args:
            validated_data (dict): The validated data containing the original URL.

        Returns:
            TinyURL: The created TinyURL instance with the generated tiny URL.
        """
        tiny_url_instance = TinyURL(**validated_data)
        tiny_url_instance.save()
        return tiny_url_instance

