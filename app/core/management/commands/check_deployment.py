"""
Management command to check deployment health
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Check deployment health and configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Deployment Health Check ==='))

        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('✓ Database connection: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Database connection: FAILED - {e}'))

        # Check environment variables
        env_vars = ['SECRET_KEY', 'DEBUG']
        for var in env_vars:
            value = getattr(settings, var, 'NOT SET')
            if var == 'SECRET_KEY':
                value = '***HIDDEN***' if value else 'NOT SET'
            self.stdout.write(f'  {var}: {value}')

        # Check static files
        self.stdout.write(f'  STATIC_ROOT: {settings.STATIC_ROOT}')
        self.stdout.write(f'  MEDIA_ROOT: {settings.MEDIA_ROOT}')

        # Check allowed hosts
        self.stdout.write(f'  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')

        self.stdout.write(self.style.SUCCESS('=== Health Check Complete ==='))
