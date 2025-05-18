import pytest

from books.models import Author, Book
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):  # noqa: ARG001
    pass


@pytest.fixture(scope="function")
def users_user_1_superuser():
    User = get_user_model()
    user = User.objects.create_superuser(
        username="admin",
        email=""
    )
    yield user
    user.delete()


@pytest.fixture(scope='function')
def admin_client_1(users_user_1_superuser):
    client = APIClient()
    token = RefreshToken.for_user(users_user_1_superuser).access_token
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
    return client


@pytest.fixture(scope='function')
def admin_client_2_unauthorized():
    client = APIClient()
    return client


@pytest.fixture(scope="function")
def users_user_2():
    User = get_user_model()
    user = User.objects.create_user(
        username="user",
        email=""
    )
    yield user
    user.delete()


@pytest.fixture(scope="function")
def books_author_1():
    author = Author.objects.create(
        name="Charles Dickens",
    )
    yield author
    author.delete()


@pytest.fixture(scope="function")
def books_book_1(books_author_1):
    book = Book.objects.create(
        title="A Tale of Two Cities",
        author=books_author_1,
    )
    yield book
    book.delete()


@pytest.fixture(scope="function")
def books_book_2_borrowed(books_author_1, users_user_2):
    book = Book.objects.create(
        title="Great Expectations",
        author=books_author_1,
        borrowed_on="2023-10-01",
        borrowed_by=users_user_2,
    )
    yield book
    book.delete()


