# Generated by Django 5.0.7 on 2024-10-27 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Timer', '0009_task_user_alter_task_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
