# Generated by Django 3.1.7 on 2023-11-06 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myDatabase', '0002_codetogeneid_ncbigeneinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrecords',
            name='supplier_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]