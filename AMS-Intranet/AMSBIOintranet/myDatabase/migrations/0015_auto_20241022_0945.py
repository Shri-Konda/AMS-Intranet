# Generated by Django 3.1.7 on 2024-10-22 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myDatabase', '0014_auto_20241022_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrecords',
            name='website_flag',
            field=models.BooleanField(blank=True, null=True, verbose_name='Website Visibility'),
        ),
    ]
