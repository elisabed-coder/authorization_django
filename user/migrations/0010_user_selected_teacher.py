# Generated by Django 5.1.2 on 2024-11-05 12:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_teacherprofile_user_delete_studentprofile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='selected_teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacher'),
        ),
    ]
