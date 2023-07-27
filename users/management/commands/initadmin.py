from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.base_user import BaseUserManager

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = "admin"
            email = "admin@ilmhona.com"
            password = 'admin123'
            print('Creating account for %s (%s)' % (username, email))
            admin = User(email=email, username=username)
            admin.is_active = True
            admin.is_admin = True
            admin.set_password(password)
            admin.save()
        else:
            print('Admin accounts can only be initialized if no User exist')
    