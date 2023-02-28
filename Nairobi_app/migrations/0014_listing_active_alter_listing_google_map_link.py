# Generated by Django 4.1.6 on 2023-03-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nairobi_app', '0013_listing_google_map_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='listing',
            name='google_map_link',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
