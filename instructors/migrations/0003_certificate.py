# Generated by Django 5.1.1 on 2024-10-21 18:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_course_instructor'),
        ('instructors', '0002_instructor_public_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_awarded', models.DateTimeField(auto_now_add=True)),
                ('certificate_file', models.FileField(upload_to='certificates/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.student')),
            ],
        ),
    ]