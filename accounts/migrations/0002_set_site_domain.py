from django.db import migrations
from django.conf import settings


def set_site_domain(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site, created = Site.objects.get_or_create(pk=settings.SITE_ID)
    
    # Auto-detect: if DEBUG, use localhost, else use ALLOWED_HOSTS
    if settings.DEBUG:
        domain = '127.0.0.1:8000'
        name = 'localhost'
    else:
        domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'example.com'
        name = domain

    site.domain = domain
    site.name = name
    site.save()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(set_site_domain, migrations.RunPython.noop),
    ]