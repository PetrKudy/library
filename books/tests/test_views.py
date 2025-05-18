from django.urls import reverse
from django.utils import timezone
from books.models import Author, Book

import pytest


class TestAuthorViewSet:
    @pytest.mark.parametrize("method,url_name", [
            ("get", "author-list"),
            ("post", "author-list"),
            ("get", "author-detail"),
            ("put", "author-detail"),
            ("patch", "author-detail"),
            ("delete", "author-detail")
        ]
    )
    def test_viewset_auth_required(
        self,
        admin_client_2_unauthorized,
        books_author_1,
        method,
        url_name,
    ):
        if url_name == "author-detail":
            url = reverse(url_name, args=[books_author_1.id])
        else:
            url = reverse(url_name)

        response = getattr(admin_client_2_unauthorized, method)(
            url, data={}, format="json"
        )

        assert response.status_code == 401

    def test_list_authors(self, admin_client_1, books_author_1):
        """
        Test the list method of the AuthorViewSet.
        """
        response = admin_client_1.get(reverse("author-list"))
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": books_author_1.id,
                "name": books_author_1.name,
            }
        ]

    def test_create_author(self, admin_client_1):
        """
        Test the create method of the AuthorViewSet.
        """
        name = "New Author"
        response = admin_client_1.post(
            reverse("author-list"),
            data={"name": name},
        )
        assert response.status_code == 201

        author = Author.objects.get()
        assert author.name == name

        assert response.json() == {
            "id": author.id,
            "name": author.name,
        }

    def test_retrieve_author(self, admin_client_1, books_author_1):
        """
        Test the retrieve method of the AuthorViewSet.
        """
        response = admin_client_1.get(reverse("author-detail", args=[books_author_1.id]))
        assert response.status_code == 200
        assert response.json() == {
            "id": books_author_1.id,
            "name": books_author_1.name,
        }

    def test_update_author(self, admin_client_1, books_author_1):
        """
        Test the update method of the AuthorViewSet.
        """
        new_name = "Updated Author"
        response = admin_client_1.patch(
            reverse("author-detail", args=[books_author_1.id]),
            data={"name": new_name},
        )
        assert response.status_code == 200

        books_author_1.refresh_from_db()
        assert books_author_1.name == new_name

        assert response.json() == {
            "id": books_author_1.id,
            "name": books_author_1.name,
        }

    def test_delete_author(self, admin_client_1, books_author_1):
        """
        Test the delete method of the AuthorViewSet.
        """
        response = admin_client_1.delete(reverse("author-detail", args=[books_author_1.id]))
        assert response.status_code == 204

        with pytest.raises(Author.DoesNotExist):
            books_author_1.refresh_from_db()


class TestBookViewSet:
    @pytest.mark.parametrize(
        "method,url_name",
        [
            ("get", "book-list"),
            ("post", "book-list"),
            ("get", "book-detail"),
            ("put", "book-detail"),
            ("patch", "book-detail"),
            ("delete", "book-detail"),
        ],
    )
    def test_viewset_auth_required(
        self,
        admin_client_2_unauthorized,
        books_book_1,
        method,
        url_name,
    ):
        if url_name == "book-detail":
            url = reverse(url_name, args=[books_book_1.id])
        else:
            url = reverse(url_name)

        response = getattr(admin_client_2_unauthorized, method)(
            url, data={}, format="json"
        )

        assert response.status_code == 401

    def test_list_books(self, admin_client_1, books_book_1, books_book_2_borrowed):
        """
        Test the list method of the BookViewSet.
        """
        response = admin_client_1.get(reverse("book-list"))
        assert response.status_code == 200
        assert response.json() == {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": books_book_1.id,
                    "title": books_book_1.title,
                    "author": books_book_1.author.id,
                    "is_borrowed": books_book_1.is_borrowed,
                },
                {
                    "id": books_book_2_borrowed.id,
                    "title": books_book_2_borrowed.title,
                    "author": books_book_2_borrowed.author.id,
                    "is_borrowed": books_book_2_borrowed.is_borrowed,
                },
            ],
        }

    def test_create_book(self, admin_client_1, books_author_1):
        """
        Test the create method of the BookViewSet.
        """
        title = "New Book"
        response = admin_client_1.post(
            reverse("book-list"),
            data={"title": title, "author": books_author_1.id},
        )
        assert response.status_code == 201

        book = Book.objects.get()
        assert book.title == title
        assert book.author == books_author_1

        assert response.json() == {
            "id": book.id,
            "title": book.title,
            "author": book.author.id,
            "is_borrowed": False
        }

    def test_retrieve_book(self, admin_client_1, books_book_1):
        """
        Test the retrieve method of the BookViewSet.
        """
        response = admin_client_1.get(reverse("book-detail", args=[books_book_1.id]))
        assert response.status_code == 200
        assert response.json() == {
            "id": books_book_1.id,
            "title": books_book_1.title,
            "author": books_book_1.author.id,
            "is_borrowed": books_book_1.is_borrowed,
        }

    def test_update_book(self, admin_client_1, books_book_1):
        """
        Test the update method of the BookViewSet.
        """
        new_title = "Updated Book"
        response = admin_client_1.patch(
            reverse("book-detail", args=[books_book_1.id]),
            data={"title": new_title},
        )
        assert response.status_code == 200

        books_book_1.refresh_from_db()
        assert books_book_1.title == new_title

        assert response.json() == {
            "id": books_book_1.id,
            "title": books_book_1.title,
            "author": books_book_1.author.id,
            "is_borrowed": books_book_1.is_borrowed,
        }

    def test_delete_book(self, admin_client_1, books_book_1):
        """
        Test the delete method of the BookViewSet.
        """
        response = admin_client_1.delete(reverse("book-detail", args=[books_book_1.id]))
        assert response.status_code == 204

        with pytest.raises(Book.DoesNotExist):
            books_book_1.refresh_from_db()

    def test_borrow_book(self, admin_client_1, books_book_1, users_user_2):
        """
        Test the borrowing method of the BookViewSet.
        """
        response = admin_client_1.patch(
            reverse("book-borrowing", args=[books_book_1.id]),
            data={"action": "borrow"},
            headers={"X-User-Id": str(users_user_2.id)},
        )
        assert response.status_code == 200

        books_book_1.refresh_from_db()
        assert books_book_1.borrowed_on == timezone.now().date()
        assert books_book_1.borrowed_by == users_user_2

        assert response.json() == {
            "id": books_book_1.id,
            "title": books_book_1.title,
            "author": books_book_1.author.id,
            "is_borrowed": True,
        }

    def test_borrow_book_already_borrowed(
        self, admin_client_1, books_book_2_borrowed, users_user_2
    ):
        """
        Test the borrowing method of the BookViewSet when the book is already borrowed.
        """
        response = admin_client_1.patch(
            reverse("book-borrowing", args=[books_book_2_borrowed.id]),
            data={"action": "borrow"},
            headers={"X-User-Id": str(users_user_2.id)},
        )
        assert response.status_code == 400
        assert response.json() == {"action": ["Book is already borrowed."]}

    def test_borrow_book_user_id_not_set(
        self, admin_client_1, books_book_1
    ):
        """
        Test the borrowing method of the BookViewSet when the user ID is not set in the header.
        """
        response = admin_client_1.patch(
            reverse("book-borrowing", args=[books_book_1.id]),
            data={"action": "borrow"},
        )
        assert response.status_code == 400
        assert response.json() == {"non_field_errors": ["User ID is not set in x-User-Id header."]}

    def test_borrow_book_user_id_not_exists(
        self, admin_client_1, books_book_1
    ):
        """
        Test the borrowing method of the BookViewSet when the user ID does not exist.
        """
        response = admin_client_1.patch(
            reverse("book-borrowing", args=[books_book_1.id]),
            data={"action": "borrow"},
            headers={"X-User-Id": "999999999"},
        )
        assert response.status_code == 400
        assert response.json() == {"non_field_errors": ["User ID in x-User-Id header not exists."]}

    def test_return_book(self, admin_client_1, users_user_2, books_book_2_borrowed):
        """
        Test the return method of the BookViewSet.
        """
        response = admin_client_1.patch(
            reverse("book-borrowing", args=[books_book_2_borrowed.id]),
            data={"action": "return"},
            headers={"X-User-Id": str(users_user_2.id)},
        )
        assert response.status_code == 200

        books_book_2_borrowed.refresh_from_db()
        assert books_book_2_borrowed.is_borrowed is False
        assert books_book_2_borrowed.borrowed_by is None
        assert books_book_2_borrowed.borrowed_on is None

        assert response.json() == {
            "id": books_book_2_borrowed.id,
            "title": books_book_2_borrowed.title,
            "author": books_book_2_borrowed.author.id,
            "is_borrowed": False,
        }

    def test_return_book_not_borrowed(
        self, admin_client_1, books_book_1, users_user_2
    ):
        """
        Test the return method of the BookViewSet when the book is not borrowed.
        """
        response = admin_client_1.patch(
            reverse("book-borrowing", args=[books_book_1.id]),
            data={"action": "return"},
            headers={"X-User-Id": str(users_user_2.id)},
        )
        assert response.status_code == 400
        assert response.json() == {"action": ["Book is not borrowed."]}

