
from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Name")
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("Title")
    )
    author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        verbose_name=_("Author")
    )
    borrowed_on = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Borrowed On")
    )
    borrowed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Borrowed By")
    )

    def __str__(self):
        return self.title

    @property
    def is_borrowed(self):
        return self.borrowed_on is not None and self.borrowed_by is not None
