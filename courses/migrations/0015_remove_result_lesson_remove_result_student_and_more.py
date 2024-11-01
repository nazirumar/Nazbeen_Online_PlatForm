# Generated by Django 5.1.1 on 2024-10-24 17:17

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_alter_enrollment_progress_watchedlesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='result',
            name='student',
        ),
        migrations.RemoveField(
            model_name='review',
            name='course',
        ),
        migrations.RemoveField(
            model_name='review',
            name='student',
        ),
        migrations.RemoveField(
            model_name='watchedlesson',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='watchedlesson',
            name='student',
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='enrollment',
            old_name='date_enrolled',
            new_name='enrollment_date',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question_text',
            new_name='text',
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('student', 'course')},
        ),
        migrations.RemoveField(
            model_name='question',
            name='marks',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.RemoveField(
            model_name='quiz',
            name='total_marks',
        ),
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('true_false', 'True / False')], default='multiple_choice', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='courses.module'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='public_id',
            field=models.CharField(blank=True, db_index=True, max_length=130, null=True),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.course'),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.student'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(default='how was your night', max_length=250),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='courses.question')),
            ],
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='WatchedLesson',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='progress',
        ),
    ]
