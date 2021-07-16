# Generated by Django 3.2.5 on 2021-07-16 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('link', models.URLField()),
                ('img_url', models.URLField()),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Advertiser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Impression',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.GenericIPAddressField()),
                ('impression_time', models.DateTimeField()),
                ('involved_ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='impression_list', to='advertising_management.ad')),
            ],
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('impression_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advertising_management.impression')),
            ],
            bases=('advertising_management.impression',),
        ),
        migrations.CreateModel(
            name='Seen',
            fields=[
                ('impression_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advertising_management.impression')),
            ],
            bases=('advertising_management.impression',),
        ),
        migrations.AddField(
            model_name='ad',
            name='ad_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to='advertising_management.advertiser'),
        ),
    ]
