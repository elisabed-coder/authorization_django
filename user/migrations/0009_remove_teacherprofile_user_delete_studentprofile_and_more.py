# Generated by Django 5.1.2 on 2024-11-04 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_studentprofile_selected_subject_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacherprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='StudentProfile',
        ),
        migrations.DeleteModel(
            name='TeacherProfile',
        ),
    ]
