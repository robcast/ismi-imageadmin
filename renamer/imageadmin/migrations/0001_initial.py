# Generated by Django 4.0.1 on 2022-01-22 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('last_access_date', models.DateTimeField(auto_now=True, verbose_name='last access')),
            ],
        ),
        migrations.CreateModel(
            name='DirEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('last_access_date', models.DateTimeField(auto_now=True, verbose_name='last access')),
                ('in_progress', models.BooleanField()),
                ('directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imageadmin.directory')),
            ],
        ),
    ]
