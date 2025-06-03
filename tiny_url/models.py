import string

from django.db import models


CHARACTERS = string.ascii_letters + string.digits


class TinyURL(models.Model):
    """
    Represents original url and its tiny form.

    Fields:
        url (URLField): the original url
        tiny_form (URLField): the tiny form
    """
    url = models.URLField(db_index=True, unique=True)
    short_code = models.CharField(max_length=10, unique=True, blank=True)

    def __str__(self) -> str:
        return f"{self.url} -> {self.short_code}"

    def _encode_short_code(self) -> str:
        """
        Encode the primary key into a short code using a base conversion.

        Returns:
            str: The encoded tiny URL.
        """
        num = self.pk
        if num == 0:
            return CHARACTERS[0]
        short_code = ''
        base = len(CHARACTERS)
        while num > 0:
            num, rem = divmod(num, base)
            short_code = CHARACTERS[rem] + short_code
        return short_code

    def save(self, *args, **kwargs) -> None:
        """
        Save the TinyURL instance, generating the tiny URL if it is a new instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if not self.pk:
            super().save(*args, **kwargs)
            self.short_code = self._encode_short_code()
            super().save(update_fields=['short_code'])
        else:
            super().save(*args, **kwargs)
