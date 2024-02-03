# Generated by Django 5.0.1 on 2024-02-03 13:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListedBooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_by_user_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, size=None)),
                ('book_name', models.CharField(max_length=512)),
                ('author_name', models.CharField(max_length=512)),
                ('is_deleted', models.BooleanField(default=False)),
                ('state_manager', models.IntegerField(default=-100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('rating', models.IntegerField()),
                ('added_by_users', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=512), blank=True, size=None)),
            ],
        ),
    ]
