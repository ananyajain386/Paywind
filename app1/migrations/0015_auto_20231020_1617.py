# Generated by Django 2.2 on 2023-10-20 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_auto_20231020_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dropdowns',
            name='delete',
            field=models.CharField(blank=True, default='False', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='dropdowns',
            name='edit',
            field=models.CharField(blank=True, default='False', max_length=20, null=True),
        ),
    ]