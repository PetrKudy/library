from django.urls import reverse
from ..models import User
import pytest


class TestObrainToken:
    def test_obrain_token_superuser(self, admin_client_2_unauthorized, users_user_1_superuser):
        user_password = "password"
        users_user_1_superuser.set_password(user_password)
        users_user_1_superuser.save()

        response = admin_client_2_unauthorized.post(
            reverse("token_obtain_pair"),
            data={
                "username": users_user_1_superuser.username,
                "password": user_password,
            },
        )
        assert response.status_code == 200
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_obrain_not_superuser(self, admin_client_2_unauthorized, users_user_2):
        user_password = "password"
        users_user_2.set_password(user_password)
        users_user_2.save()

        response = admin_client_2_unauthorized.post(
            reverse("token_obtain_pair"),
            data={
                "username": users_user_2.username,
                "password": user_password,
            },
        )
        assert response.status_code == 400

        assert response.json() == {
            "non_field_errors": ["Only staff members are allowed to obtain a token."]
        }


class TestUserViewSet:
    @pytest.mark.parametrize(
        "method,url_name",
        [
            ("get", "user-list"),
            ("post", "user-list"),
            ("get", "user-detail"),
            ("put", "user-detail"),
            ("patch", "user-detail"),
            ("delete", "user-detail"),
        ],
    )
    def test_viewset_auth_required(
        self,
        admin_client_2_unauthorized,
        users_user_1_superuser,
        method,
        url_name,
    ):
        if url_name == "user-detail":
            url = reverse(url_name, args=[users_user_1_superuser.id])
        else:
            url = reverse(url_name)

        response = getattr(admin_client_2_unauthorized, method)(
            url, data={}, format="json"
        )

        assert response.status_code == 401

    def test_list_users(self, admin_client_1, users_user_1_superuser):
        response = admin_client_1.get(reverse("user-list"))
        assert response.status_code == 200
        assert response.json() == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": users_user_1_superuser.id,
                    "username": users_user_1_superuser.username,
                    "first_name": "",
                    "last_name": "",
                    "email": users_user_1_superuser.email,
                }
            ],
        }

    def test_create_user(self, admin_client_1):
        username = "newuser"
        email = "bla@bla.com"

        response = admin_client_1.post(
            reverse("user-list"),
            data={
                "username": username,
                "email": email,
            },
        )
        assert response.status_code == 201
        user = User.objects.last()
        assert response.json() == {
            "id": user.id,
            "username": username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": email,
        }

    def test_retrieve_user(self, admin_client_1, users_user_1_superuser):
        response = admin_client_1.get(
            reverse("user-detail", args=[users_user_1_superuser.id])
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": users_user_1_superuser.id,
            "username": users_user_1_superuser.username,
            "first_name": "",
            "last_name": "",
            "email": users_user_1_superuser.email,
        }

    def test_update_user(self, admin_client_1, users_user_1_superuser):
        new_username = "updateduser"

        response = admin_client_1.patch(
            reverse("user-detail", args=[users_user_1_superuser.id]),
            data={
                "username": new_username,
            },
        )
        assert response.status_code == 200

        users_user_1_superuser.refresh_from_db()
        assert users_user_1_superuser.username == new_username

        assert response.json() == {
            "id": users_user_1_superuser.id,
            "username": new_username,
            "first_name": "",
            "last_name": "",
            "email": users_user_1_superuser.email,
        }

    def test_delete_user(self, admin_client_1, users_user_1_superuser):
        response = admin_client_1.delete(
            reverse("user-detail", args=[users_user_1_superuser.id])
        )
        assert response.status_code == 204

        with pytest.raises(User.DoesNotExist):
            users_user_1_superuser.refresh_from_db()