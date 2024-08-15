# Generated by Django 4.2.11 on 2024-05-05 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_aboutus'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('deactive', 'Deactive')], default='deactive', max_length=100),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='header_main',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='main_photo',
            field=models.ImageField(upload_to='about_us_photos/'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='text_main',
            field=models.TextField(max_length=3000),
        ),
    ]