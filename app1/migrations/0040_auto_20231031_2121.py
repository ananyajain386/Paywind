# Generated by Django 2.2 on 2023-10-31 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0039_dynamic_panel_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkedaccount',
            name='account_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]