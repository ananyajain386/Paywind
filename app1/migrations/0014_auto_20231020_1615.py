# Generated by Django 2.2 on 2023-10-20 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_dropdowns'),
    ]

    operations = [
        migrations.AddField(
            model_name='dropdowns',
            name='delete',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='dropdowns',
            name='edit',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
