# Generated by Django 4.2.11 on 2024-05-12 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=40),
        ),
    ]
