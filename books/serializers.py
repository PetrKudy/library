from rest_framework import serializers

from .models import Author, Book
from django.utils.translation import gettext_lazy as _
from users.models import User


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'name']
        read_only_fields = ['id']


class BookSerializer(serializers.ModelSerializer):

    is_borrowed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "is_borrowed"]
        read_only_fields = ["id"]


class BookBorrowingSerializer(serializers.ModelSerializer):
    """
    Serializer for borrowing a book.
    """
    BORROW_ACTION = "borrow"
    RETURN_ACTION = "return"
    action = serializers.ChoiceField(
        choices=[BORROW_ACTION, RETURN_ACTION],
        write_only=True,
    )

    class Meta:
        model = Book
        fields = ["action"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.borrowed_by_user_id = self.context["request"].headers.get("X-User-Id", None)

    def _validate_book_validity(self, value):
        if value == self.BORROW_ACTION and self.context["book"].is_borrowed:
            raise serializers.ValidationError(_("Book is already borrowed."))

        if value == self.RETURN_ACTION and not self.context["book"].is_borrowed:
            raise serializers.ValidationError(_("Book is not borrowed."))

    def _validate_borrowed_by_user_id(self, user_id):
        if not user_id:
            raise serializers.ValidationError(_("User ID is not set in x-User-Id header."))

        if not User.objects.filter(id=user_id).exists():
            raise serializers.ValidationError(_("User ID in x-User-Id header not exists."))

    def validate_action(self, value):
        """
        Validate the action field.
        """

        self._validate_book_validity(value)

        return value

    def validate(self, values):
        self._validate_borrowed_by_user_id(self.borrowed_by_user_id)
        return values
