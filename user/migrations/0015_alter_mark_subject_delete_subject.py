# Generated by Django 5.1.2 on 2024-11-05 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_subject_alter_mark_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='subject',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
