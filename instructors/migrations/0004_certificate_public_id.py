# Generated by Django 5.1.1 on 2024-10-21 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructors', '0003_certificate'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=130, null=True),
        ),
    ]
