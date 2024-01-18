# Generated by Django 2.2 on 2023-10-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0031_postpaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpaid',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postpaid',
            name='pan_card_no',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]