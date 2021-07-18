# Generated by Django 3.2.5 on 2021-07-18 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertising_management', '0002_alter_advertiser_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=15)),
                ('view_count', models.IntegerField()),
                ('click_count', models.IntegerField()),
                ('report_time', models.DateTimeField()),
            ],
        ),
    ]