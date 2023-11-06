# Generated by Django 3.1.7 on 2021-07-08 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='liveCurrencyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency', models.CharField(blank=True, max_length=64, null=True, verbose_name='FROM')),
                ('to_currency', models.CharField(blank=True, max_length=64, null=True, verbose_name='TO')),
                ('live_rate', models.FloatField(blank=True, null=True, verbose_name='Live Rate')),
            ],
            options={
                'verbose_name_plural': 'Live Rate',
            },
        ),
    ]