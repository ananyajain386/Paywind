# Generated by Django 2.2 on 2023-10-16 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_auto_20231016_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkedaccount',
            name='UPI_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]