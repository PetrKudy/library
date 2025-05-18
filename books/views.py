from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, BookBorrowingSerializer
from .filters import BookListFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = None


class BookViewSet(viewsets.ModelViewSet):
    """
    Viewset for the Book model.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookListFilter

    @action(detail=True, methods=["patch"], serializer_class=BookBorrowingSerializer)
    def borrowing(self, request, pk):
        book = get_object_or_404(self.get_queryset(), pk=pk)

        serializer = self.get_serializer_class()(data=request.data, context={"request": request, "book": book})
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["action"] == BookBorrowingSerializer.BORROW_ACTION:
            book.borrowed_on = timezone.now()
            book.borrowed_by_id = serializer.borrowed_by_user_id
        else:
            book.borrowed_on = None
            book.borrowed_by = None
        book.save()
        return Response(data=BookSerializer(book).data, status=status.HTTP_200_OK)
