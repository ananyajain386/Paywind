# Generated by Django 2.2 on 2023-10-28 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0035_dynamic_panel_state1'),
    ]

    operations = [
        migrations.AddField(
            model_name='splitbill',
            name='delete1',
            field=models.CharField(blank=True, default='false', max_length=20, null=True),
        ),
    ]