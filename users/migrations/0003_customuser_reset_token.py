# Generated by Django 5.2 on 2025-07-18 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_confirmation_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='reset_token',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
