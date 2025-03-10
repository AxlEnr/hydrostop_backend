# Generated by Django 5.1.6 on 2025-03-10 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showerCode', models.CharField(max_length=30, unique=True, verbose_name='Name of the de shower')),
                ('status', models.IntegerField(choices=[(1, 'Shower On'), (0, 'Shower Off')])),
                ('available', models.IntegerField(choices=[(1, 'Shower available'), (0, 'Shower unavailable')])),
            ],
        ),
    ]
