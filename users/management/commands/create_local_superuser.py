from django.core.management.base import BaseCommand

from users.models import User

USER_USERNAME = 'admin'
USER_PASSWORD = 'admin'


class Command(BaseCommand):
    help = 'Creates super user during project start up'

    def handle(self, *args, **options):  # noqa: ARG002
        user, _ = User.objects.get_or_create(
            username=USER_USERNAME,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            }
        )
        user.set_password(USER_PASSWORD)
        user.save()
