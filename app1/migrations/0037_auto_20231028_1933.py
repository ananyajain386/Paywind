# Generated by Django 2.2 on 2023-10-28 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0036_splitbill_delete1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='PIN',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='linkedaccount',
            name='PIN',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
