import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Renderのダッシュボードの「Key」に合わせる
        username = os.environ.get('SUPERUSER_NAME') 
        password = os.environ.get('SUPERUSER_PASS')

        # 念のため、環境変数が取得できているかチェック
        if not username or not password:
            self.stdout.write("Error: SUPERUSER_NAME or SUPERUSER_PASS is not set in Environment.")
            return

        # 修正：固定値 'akm_vvvr' ではなく取得した変数 username でチェック
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email='',
                password=password
            )
            self.stdout.write(f"Successfully created superuser: {username}")
        else:
            self.stdout.write(f"Superuser {username} already exists.")