# Generated by Django 5.0.2 on 2024-03-12 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_question_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
