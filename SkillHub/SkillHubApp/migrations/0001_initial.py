# Generated by Django 5.1.3 on 2024-11-22 19:43

import SkillHubApp.models
import ckeditor.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=200, null=True)),
                ("content", ckeditor.fields.RichTextField(max_length=800)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "media_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="post_media/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=[
                                    "jpg",
                                    "jpeg",
                                    "png",
                                    "gif",
                                    "webp",
                                    "mp4",
                                    "avi",
                                    "mov",
                                    "mkv",
                                    "webm",
                                    "mp3",
                                    "wav",
                                    "ogg",
                                    "m4a",
                                    "pdf",
                                    "doc",
                                    "docx",
                                    "txt",
                                    "rtf",
                                ]
                            ),
                            SkillHubApp.models.validate_file_size,
                        ],
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("professional", "Profesional"),
                            ("company", "Empresa"),
                        ],
                        default="professional",
                        max_length=20,
                    ),
                ),
                ("bio", models.TextField(blank=True, null=True)),
                ("location", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Connection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pendiente"),
                            ("accepted", "Aceptado"),
                            ("rejected", "Rechazado"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "from_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connections_sent",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "to_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connections_received",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("from_user", "to_user")},
            },
        ),
    ]
