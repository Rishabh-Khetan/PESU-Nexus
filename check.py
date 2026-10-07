import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PESUNexus.settings')
django.setup()

from django.apps import apps
from django.conf import settings

print("Using DB:", settings.DATABASES['default']['ENGINE'])
print("DB Name:", settings.DATABASES['default'].get('NAME'))
print("---")

app = apps.get_app_config('materials')
for model in app.get_models():
    try:
        count = model.objects.count()
        print(f"{model._meta.db_table}: {count} rows")
    except Exception as e:
        print(f"{model._meta.db_table}: ERROR - {e}")
        