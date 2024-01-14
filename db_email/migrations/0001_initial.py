# Generated by Django 4.2.9 on 2024-01-12 14:21

import db_email.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.TextField(blank=True)),
                ('body', models.TextField(blank=True)),
                ('from_email', db_email.fields.EmailField(max_length=254)),
                ('to', db_email.fields.MultiEmailField()),
                ('cc', db_email.fields.MultiEmailField(blank=True)),
                ('bcc', db_email.fields.MultiEmailField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mimetype', models.CharField(blank=True, max_length=254)),
                ('file', models.FileField(blank=True, upload_to='db_email')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='db_email.email')),
            ],
        ),
        migrations.CreateModel(
            name='EmailAlternative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('mimetype', models.CharField(blank=True, max_length=254)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alternatives', to='db_email.email')),
            ],
        ),
    ]